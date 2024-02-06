import pandas as pd
import plotly.graph_objects as go


class PlottingService:
    def plot_absolute(self, data: pd.DataFrame, title='Absolute Values by Country and Year', yaxis_title='Value'):
        """
        Plot the absolute values for each country over the years.
        """
        fig = go.Figure()
        for index, row in data.iterrows():
            country = row['country name']
            fig.add_trace(go.Scatter(x=data.columns[3:], y=row[3:],
                                     mode='lines+markers', name=country))

        fig.update_layout(title=title, xaxis_title='Year', yaxis_title=yaxis_title)
        fig.show()

    def plot_relative(self, data, title='Relative Values by Country and Year', yaxis_title='Relative Value'):
        """
        Calculate and plot the relative values for each country per year.
        """
        relative_data = data.copy()
        # Calculate the total for each year across all countries
        totals = relative_data.iloc[:, 3:].sum()

        # Calculate relative values
        for year in relative_data.columns[3:]:
            relative_data[year] = relative_data[year] / totals[year] * 100

        fig = go.Figure()
        for index, row in relative_data.iterrows():
            country = row['country name']
            fig.add_trace(go.Scatter(x=relative_data.columns[3:], y=row[3:],
                                     mode='lines+markers', name=country))

        fig.update_layout(title=title, xaxis_title='Year', yaxis_title=yaxis_title)
        fig.show()


plotting_service = PlottingService()
