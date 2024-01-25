# read dta file and visualize it

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import plotly.graph_objects as go

ds = pd.read_stata('TRADHIST_v4.dta')
print(ds.head())
print(ds.columns)
