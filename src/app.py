from flask import Flask, render_template
from processing.signal import Signal
from processing.ecg.ecg_signal import ECGSignal
from processing.eda.eda_signal import EDASignal
from database import get_database_connection, insert_signal_data, insert_extracted_feature
from bokeh.embed import components
from bokeh.resources import CDN

def pair(a, b):
    return zip(a, b)

app = Flask(__name__)

app.jinja_env.filters['pair'] = pair

# Load the signal data
#signal_data_ecg = Signal.load_static_signal("../signals/staticopensignalsdata.txt", "CH1")
signal_data_eda = Signal.load_static_signal("../signals/staticopensignalsdata.txt", "CH5")

# Create instances of ECGSignal and EDASignal
#ecg = ECGSignal(signal_data_ecg.header, signal_data_ecg.signal_data, signal_data_ecg.sampling_rate)
eda = EDASignal(signal_data_eda.header, signal_data_eda.signal_data, signal_data_eda.sampling_rate)

# Preprocess the signal data
#ecg.preprocess_signal()
eda.preprocess_signal()

# Extract features from the signal data
#ecg_features = ecg.extract_features()
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
    # Generate Bokeh CSS and JS links from CDN
    bokeh_js = CDN.js_files[0]
    
    # Get the visualization and features HTML code for each step
    visualizations = []
    for step_index in range(len(eda.signal_data_history)):
        visualization = eda.get_visualization(step_index)
        visualizations.append(visualization)
        
    # Generate script and div components for each Bokeh plot
    scatter_scripts = []
    scatter_divs = []
    for visualization in visualizations:
        if visualization is not None:
            script, div = components(visualization)
            scatter_scripts.append(script)
            scatter_divs.append(div)

    return render_template(
        'index.html',
        edr_amplitude=eda_features.get('EDR Amplitude'),
        edr_rising_time=eda_features.get('EDR Rising Time (Rise Time)'),
        edr_response_peak=eda_features.get('EDR Response Peak (Peak Time)'),
        latency_to_stimulus=eda_features.get('Latency to Stimulus (onset)'),
        recovery_time_50=eda_features.get('Recovery Time to 50% Amplitude'),
        recovery_time_63=eda_features.get('Recovery Time to 63% Amplitude'),
        scatter_divs=scatter_divs,
        scatter_scripts=scatter_scripts,
        bokeh_js=bokeh_js
    )

if __name__ == '__main__':
        # Start data streaming
    eda.start_data_streaming()
    
    app.run(debug=True)