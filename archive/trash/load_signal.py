"""
Module/Script Name: Load Bio-Signal
Author: Jonas Bucksch
Created: 20.06.2023
Last Modified: 15.07.2023

Description: Loading the acquired Bio-Signal
"""

# import biosignalsnotebooks as bsnb

# def load_signal(path:str, channel:str,**kwargs) -> Signal:
    
#     # Load entire acquisition data.
#     data, header = bsnb.load(path, get_header=True, **kwargs)

#     # Store the desired channel (CH3) in the "signal" variable
#     signal = data[channel]

#     # Sampling rate definition.
#     sr = header["sampling rate"]

#     # Raw to uS sample value conversion.
#     signal_us = bsnb.raw_to_phy("EDA", "bioplux", signal, 12, "uS")
    
#     return Signal(signal_us, sr)
