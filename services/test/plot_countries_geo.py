import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Import data from GitHub
data1 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_with_codes.csv')
data2 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')

# fig = go.Figure(data=go.Choropleth(
#     locations = data2['CODE'],
#     z = data2['GDP (BILLIONS)'],
#     text = data2['COUNTRY'],
#     # colorscale = 'Blues',
#     # autocolorscale=False,
#     # reversescale=True,
#     # marker_line_color='darkgray',
#     # marker_line_width=0.5,
#     # colorbar_tickprefix = '$',
#     # colorbar_title = 'GDP<br>Billions US$',
# ))


# Create basic choropleth map
fig = px.choropleth(data2, locations='CODE',
                    color='GDP (BILLIONS)',
                    hover_name='COUNTRY',
                    projection='natural earth',
                    title='GDP by Country')
# lock the geographical scope to Europe
# fig.update_geos(visible=False, showcountries=True, countrycolor="Black")
# fig.update_layout(geo_scope='europe')

# fig = px.choropleth(data1,
#                     locations='iso_alpha',
#                     color='gdpPercap',
#                     hover_name='country',
#                     projection='natural earth', animation_frame='year',
#                     title='GDP per Capita by Country')
fig.show()
