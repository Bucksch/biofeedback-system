import unittest
import pytest
from src.processing.signal import Signal

class LoadSignalTestCase(unittest.TestCase):
    def test_load_signal(self):
        # Specify the path and channel for testing
        path = "signals/staticopensignalsdata.txt"
        channel = "CH1"

        # Call the load_signal() method
        signal_data = Signal.load_signal(path, channel)

        # Verify that the signal_data is an instance of the Signal class
        self.assertIsInstance(signal_data, Signal)

        # Verify that the signal_data attributes are correctly populated
        self.assertIsNotNone(signal_data.signal_data)
        self.assertIsNotNone(signal_data.sampling_rate)
        # Add more assertions if necessary

        # Perform additional tests or assertions based on your requirements
        
    def test_load_signal_invalid_path(self):
        # Test case for an invalid file path
        path = ""
        channel = "CH1"

        # Verify that an appropriate exception is raised
        with self.assertRaises(FileNotFoundError):
            Signal.load_signal(path, channel)

    @pytest.mark.parametrize("channel", ["InvalidChannel"])
    def test_load_signal_invalid_channel(channel):
        # Test case for an invalid channel
        path = "signals/staticopensignalsdata.txt"

        # Use pytest's `raises` context manager to assert the raised exception
        with pytest.raises(KeyError) as excinfo:
            Signal.load_signal(path, channel)

        # Assert that the expected partial error message is in the raised exception
        expected_error_message = f"Channel '{channel}' not found in the data."
        assert expected_error_message in str(excinfo.value)

    # Add more test cases as necessary

if __name__ == '__main__':
    unittest.main()