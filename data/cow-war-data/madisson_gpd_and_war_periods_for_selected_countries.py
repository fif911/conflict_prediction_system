"""Maddison GDP and conflict periods for selected countries by type of conflict"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

from war_periods_for_selected_countries import get_major_conflicts_periods

# An extra-state war involves fighting by a state system member outside its borders against
# the armed forces of an entity that is not a member of the interstate system
# Colonial--conflict with colony (war type 2)
# Imperial--state vs. nonstate (war type 3)
ds1 = pd.read_csv('Extra-StateWarData_v4.0.csv', encoding='cp1252')
# Wars between states (type 1)
ds2 = pd.read_csv('Inter-StateWarData_v4.0.csv', encoding='cp1252')
# Uprisings and Revolutions
#  Civil wars for central control (war type 4)
#  Civil wars  over local issues (war type 5)
# Regional internal (war type 6)
# Intercommunal (war type 7)
ds3 = pd.read_csv('Intra-StateWarData_v4.1.csv', encoding='cp1252')
# Non-state wars
# In nonstate territory (war type 8)
# Across state borders (war type 9)
# ds4 = pd.read_csv('Non-StateWarData_v4.0.csv', encoding='cp1252')
gdp_ds = pd.read_excel('../Maddison/mpd2020.xlsx', sheet_name='Full data')

# get the list of conflicts for the countries of interest and plot by type of the conflict
# USA, United Kingdom, Germany, France, Russia, China, Turkey, Netherlands, Spain
CODES = [2, 200, 255, 220, 365, 710, 640, 210, 230]
COUNTRIES = ['USA', 'United Kingdom', 'Germany', 'France', 'Russia', 'China', 'Turkey', 'Netherlands', 'Spain']
MAD_GDP_CODES = ["USA", "GBR", "DEU", "FRA", "SUN", "CHN", "TUR", "NLD", "ESP"]

MAX_GDP_PER_CAPITA = 60_000
MAX_GDP = 20_000_000_000

for ccode, cname, mad_ccode in zip(CODES, COUNTRIES, MAD_GDP_CODES):
    ds1_country = ds1[(ds1['ccode1'] == ccode) | (ds1['ccode2'] == ccode)]
    ds2_country = ds2[(ds2['ccode'] == ccode)]
    ds3_country = ds3[(ds3['CcodeA'] == ccode) | (ds3['CcodeB'] == ccode)]

    mad_gdp_country = gdp_ds[gdp_ds['countrycode'] == mad_ccode]
    mad_gdp_country = mad_gdp_country.set_index('year')
    # drop the years before 1700
    mad_gdp_country = mad_gdp_country[mad_gdp_country.index >= 1650]
    # add GDP column as GDP per capita * population
    # interpolate the missing values
    # .fillna(
    #     mad_gdp_country['gdppc'].interpolate(method="spline",order=3, limit_direction="both", limit=None)
    # )
    mad_gdp_country['gdppc'] = mad_gdp_country['gdppc'].interpolate(limit_direction="both")
    mad_gdp_country['pop'] = mad_gdp_country['pop'].interpolate(limit_direction="both")
    mad_gdp_country['GDP'] = mad_gdp_country['gdppc'] * mad_gdp_country['pop']

    # generate an ascending series similar to country GDP

    # ----- MAJOR CONFLICTS HIGHLIGHTED -----
    start_years, end_years = get_major_conflicts_periods(ds1_country, ds2_country, ds3_country)

    fig, ax = plt.subplots()
    ax.plot(mad_gdp_country['GDP'].index, mad_gdp_country['GDP'].values, color='red', ms=10)
    ax.set_ylabel('GDP', color='red')
    ax.set_ylim(0, MAX_GDP)
    # plot gdp per capita as second graph with scale on the right
    ax2 = ax.twinx()
    ax2.plot(mad_gdp_country['GDP'].index, mad_gdp_country['gdppc'].values, color='blue', ms=10)
    ax2.set_ylabel('GDP per capita', color='blue')
    ax2.set_ylim(0, MAX_GDP_PER_CAPITA)

    for start, end in zip(start_years, end_years):
        ax.axvspan(start, end, alpha=0.5, color='black')
    plt.title(f'{cname} major conflict periods and Maddison GDP')
    # show only since 1820
    plt.xlim(1820, 2020)
    plt.show()

# TODO add data about famines periods and their severity https://ourworldindata.org/famines#the-our-world-in-data-dataset-of-famines
