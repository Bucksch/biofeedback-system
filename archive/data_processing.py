import h5py
import numpy as np
import pandas as pd
import bokeh.plotting._figure
import biosignalsnotebooks as bsnb
from opensignalsreader import OpenSignalsReader as osr
from numpy import average, array, reshape, sqrt, sort, diff, where, argmax, max
from numbers import Number
from scipy import signal
# biosignalsnotebooks own package.
import biosignalsnotebooks as bsnb
# Scientific programming package.
from numpy import average, array, reshape, sqrt, sort, diff, where, argmax, max
from numbers import Number
# Gaussian Distribution function.
from scipy.stats import norm
from copy import deepcopy

data, header = bsnb.load("../../../archive/data/staticopensignalsdata.txt", get_header=True)

h5 = h5py.File("../../../archive/data/staticopensignalsdata.h5")
print(h5.keys())

dataset = h5['00:07:80:4C:03:E8']
keys = dataset.keys
print(keys)
print(dataset.items)

data = osr("../../../archive/data/staticopensignalsdata.txt")
# Access single sensor signal using the sensor's channel number
data.raw(5)
data.signal(5)

# Access single sensor signal using the sensor's label
data.raw("ECG")
data.signal("ECG")

# Access multiple sensor signals using the channel numbers (here: channel 1 & 2)
data.raw([1,5])
data.signal([1,5])

# Access multiple sensor signals using the sensor labels (here: channel 1 & 2)
data.raw(["ECG", "EDA"])
data.signal(["ECG", "EDA"])

# Read OpenSignals file and plot all signals
#data = osr("../../../archive/data/staticopensignalsdata.txt", show=True)

# Read OpenSignals file and plot all raw signals.
data = osr("../../../archive/data/staticopensignalsdata.txt", show=True, raw=True)

# Plot ECG signal using the channel number
data.plot('ECG')

# Plot ECG signal using the sensor label
data.plot(1)

# Plotting multiple signals using the channel number
#data.plot(['ECG', 'staticopensignalsdata'])

# Plotting multiple signals using the sensor label
#data.plot([1, 5])

# Plot raw ECG data
data.plot('ECG', raw=True)