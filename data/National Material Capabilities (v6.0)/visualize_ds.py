# read dataset from csv file and visualize it
# the data is from https://correlatesofwar.org/data-sets/national-material-capabilities
# plot each country's military expenditure and population

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import plotly.graph_objects as go

# read data from csv file
data = pd.read_csv('NMC-60-abridged/NMC-60-abridged.csv')

fig = go.Figure()

# map country code to country full name
country_code = pd.read_csv('NMC-60-abridged/COW-country-codes.csv')
country_code = country_code[['StateAbb', 'StateNme']]
country_code = country_code.set_index('StateAbb')
country_code = country_code.to_dict()['StateNme']
# merge country full name to data
data['stateabb'] = data['stateabb'].map(country_code)
# plot each country's cinc
for i in data.stateabb.unique():
    country = data[data.stateabb == i]
    fig.add_trace(go.Scatter(x=country.year, y=country.cinc, mode='lines', name=i))

    # plt.plot(country.year, country.cinc, label=country.stateabb.iloc[0])
    # plot with Go
fig.update_layout(title='CINC of each country', xaxis_title='year', yaxis_title='CINC')
fig.show()
