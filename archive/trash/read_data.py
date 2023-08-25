import pandas as pd
from opensignalsreader import OpenSignalsReader

data = OpenSignalsReader("../data/eda.txt")

data.signal("ECG")