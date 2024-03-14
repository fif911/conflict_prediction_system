import pandas as pd
import plotly.graph_objects as go

from services.plotting import plotting_service

# Load the dataset
file_path = 'hc_human_capital_by_country_and_year_1870_2010.csv'  # Replace with your file path
data = pd.read_csv(file_path)
# read population data
# population = pd.read_csv('population_by_country_and_year.csv')
# # human capital per capita
# data = data.set_index('Country')
# population = population.set_index('Country')
# data = data.div(population)
# data = data.reset_index()
# print(data.head())

# plotting_service.plot_absolute(data)
plotting_service.plot_relative(data, title="Human Capital relative from 1870 to 2010")
