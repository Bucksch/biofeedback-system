import biosignalsnotebooks as bsnb

class Signal:
    def __init__(self, header, signal_data, sampling_rate):
        self.header = header
        self.signal_data = signal_data
        self.sampling_rate = sampling_rate
        
    @classmethod
    def load_static_signal(cls, path: str, channel: str) -> 'Signal':
        print(f"Loading signal data from channel {channel}...")
        # Load entire acquisition data.
        try:
            data, header = bsnb.load(path, get_header=True)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{path}' not found.")

        # Store the desired channel in the "signal" variable
        try:
            signal = data[channel]
        except KeyError:
            raise KeyError(f"Channel '{channel}' not found in the data.")

        # Sampling rate definition.
        sr = header["sampling rate"]

        # Raw to uS sample value conversion.
        signal_us = bsnb.raw_to_phy("EDA", "bioplux", signal, 10, "uS")

        # Create and return a Signal instance with the loaded and processed signal
        signal_instance = cls(header, signal_us, sr)
        return signal_instance