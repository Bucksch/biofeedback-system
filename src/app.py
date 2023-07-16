from flask import Flask, render_template
from processing.signal import Signal
from processing.ecg.ecg_signal import ECGSignal
from processing.eda.eda_signal import EDASignal

app = Flask(__name__)

@app.route('/')
def home():
    # Load the signal data
    signal_data_ecg = Signal.load_signal("../signals/staticopensignalsdata.txt", "CH1")
    signal_data_eda = Signal.load_signal("../signals/staticopensignalsdata.txt", "CH5")

    # Create instances of ECGSignal and EDASignal
    ecg = ECGSignal(signal_data_ecg.signal_data, signal_data_ecg.sampling_rate)
    eda = EDASignal(signal_data_eda.signal_data, signal_data_eda.sampling_rate)

    # Preprocess the signal data
    ecg.preprocess_signal()
    eda.preprocess_signal()

    # Extract features from the signal data
    ecg_features = ecg.extract_features()
    eda_features = eda.extract_features()

    # Accessing the extracted features
    eda.print_features()

    # Get the visualization and features HTML code
    eda_visualization = eda.get_visualization(1)
    eda_features_html = eda.get_features_html()

    return render_template('home.html', eda_visualization=eda_visualization, eda_features_html=eda_features_html)

if __name__ == '__main__':
    app.run()