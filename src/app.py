from flask import Flask, render_template
from processing.signal import Signal
from processing.ecg.ecg_signal import ECGSignal
from processing.eda.eda_signal import EDASignal
from database import get_database_connection, insert_signal_data, insert_extracted_feature

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
eda.print_features()

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

    return render_template('index.html', eda_visualization=eda_visualization, eda_features_html=eda_features_html)
    pass

if __name__ == '__main__':
    app.run()