from flask import Flask, render_template
from processing.signal import Signal
from processing.ecg.ecg_signal import ECGSignal
from processing.eda.eda_signal import EDASignal
from database import get_database_connection, insert_signal_data, insert_extracted_feature
from bokeh.plotting._figure import figure
from bokeh.embed import components
from bokeh.resources import CDN

#Example for Bokeh plot, delete later!
def create_scatter_plot():
    # Create the plot
    p = figure(title="Scatter Plot", x_axis_label="X", y_axis_label="Y")
    p.scatter([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=10, color="navy")
    p.sizing_mode = "scale_both"
    # Generate the script and div components of the plot
    script, div = components(p)
    return script, div

app = Flask(__name__)

# Load the signal data
signal_data_ecg = Signal.load_static_signal("../signals/staticopensignalsdata.txt", "CH1")
signal_data_eda = Signal.load_static_signal("../signals/staticopensignalsdata.txt", "CH5")

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
#eda.print_features()
print("\n================================================")

connection = get_database_connection()

# Store preprocessed signal data in the database
# for time, value in eda:
#     insert_signal_data(connection, time, value)

# Store extracted features in the database
for feature, value in eda_features.items():
    insert_extracted_feature(connection, feature, value)

connection.close()

@app.route('/')
def index():
    # Get the visualization and features HTML code
    eda_visualization = eda.get_visualization(1)
    eda_features_html = eda.get_features_html()
    
    scatter_script1, scatter_div1 = create_scatter_plot()
    scatter_script2, scatter_div2 = create_scatter_plot()
    scatter_script3, scatter_div3 = create_scatter_plot()
    scatter_script4, scatter_div4 = create_scatter_plot()
    
    # Generate Bokeh CSS and JS links from CDN
    bokeh_js = CDN.js_files[0]

    return render_template(
        'index.html',
        eda_visualization=eda_visualization,
        eda_features_html=eda_features_html,
        edr_amplitude=eda_features.get('EDR Amplitude'),
        edr_rising_time=eda_features.get('EDR Rising Time (Rise Time)'),
        edr_response_peak=eda_features.get('EDR Response Peak (Peak Time)'),
        latency_to_stimulus=eda_features.get('Latency to Stimulus (onset)'),
        recovery_time_50=eda_features.get('Recovery Time to 50% Amplitude'),
        recovery_time_63=eda_features.get('Recovery Time to 63% Amplitude'),
        scatter_div1=scatter_div1,
        scatter_div2=scatter_div2,
        scatter_div3=scatter_div3,
        scatter_div4=scatter_div4,
        scatter_script1=scatter_script1,
        scatter_script2=scatter_script2,
        scatter_script3=scatter_script3,
        scatter_script4=scatter_script4,
        bokeh_js=bokeh_js
    )

if __name__ == '__main__':
    app.run(debug=True)