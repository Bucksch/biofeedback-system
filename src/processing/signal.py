import biosignalsnotebooks as bsnb

class Signal:
    def __init__(self, signal_data, sampling_rate):
        self.signal_data = signal_data
        self.sampling_rate = sampling_rate
        
    @classmethod
    def load_signal(cls, path: str, channel: str) -> 'Signal':
        print(f"Loading Signal Data from Channel {channel}...")
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
        signal_instance = cls(signal_us, sr)
        signal_instance.signal_data = signal_us
        signal_instance.sampling_rate = sr
        return signal_instance