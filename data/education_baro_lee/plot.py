import pandas as pd
import plotly.graph_objects as go

# Load the dataset
file_path = 'human_capital_by_country_and_year.csv'  # Replace with your file path
data = pd.read_csv(file_path)


# Function to plot the series for each country
def plot_series(data):
    fig = go.Figure()
    for country in data['Country']:
        fig.add_trace(go.Scatter(x=data.columns[1:], y=data[data['Country'] == country].iloc[0, 1:],
                                 mode='lines+markers', name=country))

    fig.update_layout(title='Human Capital by Country and Year', xaxis_title='Year', yaxis_title='Value')
    fig.show()


# Function to plot the relative value of the world share in that particular year
def plot_relative_series(data):
    # Calculate the sum for each year to determine the world share
    world_share = data.iloc[:, 1:].sum(axis=0)

    # Creating a dataframe for relative values
    relative_data = data.copy()
    for year in data.columns[1:]:
        relative_data[year] = data[year] / world_share[year]

    # Plotting
    fig = go.Figure()
    for country in relative_data['Country']:
        fig.add_trace(
            go.Scatter(x=relative_data.columns[1:], y=relative_data[relative_data['Country'] == country].iloc[0, 1:],
                       mode='lines+markers', name=country))

    fig.update_layout(title='Relative Human Capital by Country and Year', xaxis_title='Year',
                      yaxis_title='Relative Value')
    fig.show()


# Plotting the series for each country
plot_series(data)

# Plotting the relative value of the world share in that particular year
plot_relative_series(data)
