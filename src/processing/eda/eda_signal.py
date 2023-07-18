import threading
import time
from copy import deepcopy
from numbers import Number

import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.plotting._figure import figure
from flask import Markup
from numpy import argmax, array, average, diff, max, reshape, sort, sqrt, where
from pywt import iswt, swt
from scipy.stats import norm
from sklearn.mixture import GaussianMixture
from bokeh.embed import components
from bokeh.plotting import curdoc

import biosignalsnotebooks as bsnb
from processing.signal import Signal
from flask_socketio import emit
from flask import current_app

class EDASignal(Signal):
    def __init__(self, header, signal_data, sampling_rate):
        super().__init__(header, signal_data, sampling_rate)
        self.original_signal_data = signal_data # Current state of signal data
        self.signal_data_history = [signal_data] # History of signal data preprocessing steps
        self.features = {}  # Empty dictionary to store the extracted features

    def preprocess_signal(self) -> "EDASignal":
        self._apply_bandpass_filter()
        self._apply_lowpass_filter()
        self._apply_wavelet_decomposition()
        self._apply_gaussian_mixture_model()
        self._apply_thresholding()
        self._apply_inverse_wavelet_transform()
        self._apply_moving_average_smoothing()
        self._rescale_signal()
        
        return self
    
    def _apply_bandpass_filter(self):
        print("\nApplying 1st order Butterworth bandpass filter...")
        self.signal_data = bsnb.bandpass(self.signal_data, 0.045, 0.25, order=1, fs=self.sampling_rate, use_filtfilt=True)
        self._update_signal_data_history()
    
    def _apply_lowpass_filter(self):
        print("Applying 2nd order Butterworth lowpass filter...")
        self.signal_data = bsnb.lowpass(self.signal_data, 35, order=2, fs=self.sampling_rate, use_filtfilt=True)
        #self._update_signal_data_history()
    
    def _apply_wavelet_decomposition(self):
        print("Applying SWT 8th level decomposition using 'Haar' mother wavelet...")
        swt_orig_coeffs = swt(self.signal_data[:32768], "haar", level=8)
        self.detail_coeffs = swt_orig_coeffs[0][1]
        self.scaling_coeffs = swt_orig_coeffs[0][0]
    
    def _apply_gaussian_mixture_model(self):
        print("Applying Gaussian Mixture Model to detail coefficients...")
        gaussian_mixt = GaussianMixture(n_components=2, covariance_type="spherical")
        detail_coeffs_col = reshape(self.detail_coeffs, (len(self.detail_coeffs), 1))
        gaussian_mixt.fit(detail_coeffs_col)
        
        self.gaussian_mixt = gaussian_mixt
    
    def _apply_thresholding(self):
        print("Applying thresholding to detail coefficients...")
        sort_detail_coeffs = sort(self.detail_coeffs)
        norm_1 = norm(loc=self.gaussian_mixt.means_[0][0], scale=np.sqrt(self.gaussian_mixt.covariances_[0]))
        norm_2 = norm(loc=self.gaussian_mixt.means_[1][0], scale=np.sqrt(self.gaussian_mixt.covariances_[1]))
        weight_1 = self.gaussian_mixt.weights_[0]
        weight_2 = self.gaussian_mixt.weights_[1]
        
        norm_1_cdf = norm_1.cdf(sort_detail_coeffs)
        norm_2_cdf = norm_2.cdf(sort_detail_coeffs)
        
        cdf_mixt = weight_1 * norm_1_cdf + weight_2 * norm_2_cdf
        art_prop = 0.01
        low_thr = None
        high_thr = None
        
        for i in range(len(norm_1_cdf)):
            if cdf_mixt[i] - cdf_mixt[0] >= art_prop and low_thr is None:
                low_thr = sort_detail_coeffs[i]
            if cdf_mixt[-1] - cdf_mixt[i] <= art_prop and high_thr is None:
                high_thr = sort_detail_coeffs[i]
        
        filt_detail_coeffs = deepcopy(self.detail_coeffs)
        for j in range(len(filt_detail_coeffs)):
            if filt_detail_coeffs[j] <= low_thr or filt_detail_coeffs[j] >= high_thr:
                filt_detail_coeffs[j] = 0
        
        self.swt_coeffs = [(array(self.scaling_coeffs), array(filt_detail_coeffs))]
    
    def _apply_inverse_wavelet_transform(self):
        print("Applying inverse SWT to reconstruct the signal...")
        rec_signal = iswt(self.swt_coeffs, "haar")
        self.signal_data = rec_signal
        self._update_signal_data_history()
    
    def _apply_moving_average_smoothing(self):
        print("Applying moving average smoothing...")
        window_size = int(self.sampling_rate * 3)
        self.signal_data = bsnb.smooth(self.signal_data, window_size)
        #self._update_signal_data_history()
    
    def _rescale_signal(self):
        print("Rescaling the signal...")
        scaling_factor = max(self.signal_data) / max(self.original_signal_data)
        self.signal_data = self.signal_data * scaling_factor
        #self._update_signal_data_history()
    
    def _update_signal_data_history(self):
        self.signal_data_history.append(deepcopy(self.signal_data))

    def extract_features(self):
        print("Extracting features...")
        param_dict = {}

        # Latency to stimulus onset
        signal_2nd_der = diff(diff(self.signal_data))
        response_sample = argmax(signal_2nd_der)
        response_time = response_sample / self.sampling_rate
        param_dict["Latency to Stimulus (onset)"] = response_time

        # EDR amplitude
        eda_max = max(self.signal_data)
        eda_basal = self.signal_data[response_sample]
        param_dict["EDR Amplitude"] = eda_max - eda_basal

        # EDR rising time (Rise Time)
        eda_max_sample = argmax(self.signal_data)
        eda_max_time = eda_max_sample / self.sampling_rate
        param_dict["EDR Rising Time (Rise Time)"] = eda_max_time - response_time

        # EDR response peak (Peak Time)
        param_dict["EDR Response Peak (Peak Time)"] = eda_max_time

        # Recovery time to 50% amplitude
        time_50 = self._calculate_recovery_time(eda_max, 0.50, param_dict)
        param_dict["Recovery Time to 50% Amplitude"] = time_50 - eda_max_time if time_50 is not None else None

        # Recovery time to 63% amplitude
        time_63 = self._calculate_recovery_time(eda_max, 0.63, param_dict)
        param_dict["Recovery Time to 63% Amplitude"] = time_63 - eda_max_time if time_63 is not None else None
        
        self.features = param_dict

        return param_dict

    def _calculate_recovery_time(self, eda_max, amplitude_ratio, param_dict):
        start_index = argmax(self.signal_data)
        for i in range(start_index, len(self.signal_data)):
            if self.signal_data[i] <= eda_max - amplitude_ratio * param_dict["EDR Amplitude"]:
                return i / self.sampling_rate
        return None
    
    def print_features(self):
        print("\nExtracted EDA-Features:")
        for feature, value in self.features.items():
            print(f"{feature}: {value}")

    def get_features_html(self):
        html = "<ul class='feature-list'>"
        for feature, value in self.features.items():
            if value is not None:
                html += f"<li><span class='feature-name'>{feature}:</span> <span class='feature-value'>{value:.2f}</span></li>"
            else:
                html += f"<li><span class='feature-name'>{feature}:</span> <span class='feature-value'>None</span></li>"
        html += "</ul>"
        return html
    
    def get_visualization(self, step_index):
        # Access the signal history
        if step_index < len(self.signal_data_history):
            # Generating time for time axis
            time = bsnb.generate_time(self.signal_data_history[step_index], self.sampling_rate)
            signal_data = self.signal_data_history[step_index]
        else:
            # Handle invalid index
            return None

        # Create a Bokeh figure
        p = figure(title=f"EDA Signal - Step {step_index + 1}", x_axis_label="Time", y_axis_label="Amplitude")

        # Create a ColumnDataSource for Bokeh
        source = ColumnDataSource(data={"time": time, "amplitude": signal_data})

        # Add a line glyph to the figure
        p.line(x="time", y="amplitude", source=source, line_color="#1B9783")
        #p.sizing_mode="scale_width"

        return p
    
    def start_data_streaming(self, socketio):
        # Create a new thread for data streaming
        thread = threading.Thread(target=self._data_streaming_thread, args=(socketio,))
        thread.start()

    def _data_streaming_thread(self, socketio):
        # Simulate data streaming
        chunk_size = 1000  # Adjust the chunk size as needed
        delay = 1 / self.sampling_rate  # Delay between chunks based on sampling rate

        for i in range(0, len(self.signal_data), chunk_size):
            chunk = self.signal_data[i:i + chunk_size]

            # Update the plot visualization with the current chunk of data
            visualization = self.get_stream_visualization(chunk)
            script, div = components(visualization)
            socketio.emit('update_plot', {'stream_div': div, 'stream_script': script}, namespace='/')

            # Sleep to simulate real-time streaming
            time.sleep(delay)
            
    def get_stream_visualization(self, data_chunk):
        # Generating time for time axis
        time = bsnb.generate_time(data_chunk, self.sampling_rate)
        
        # Create a Bokeh figure
        p = figure(title="Simulated Data Stream", x_axis_label="Time", y_axis_label="Amplitude")

        # Create an empty data source for the stream plot
        source = ColumnDataSource(data={"time": time, "amplitude": data_chunk})

        # Add a line glyph to the figure using the empty data source
        p.line(x="time", y="amplitude", source=source)

        return p