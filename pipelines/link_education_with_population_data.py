import os

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

print(os.getcwd())
population_per_country = pd.read_csv(
    "../data/Maddison/maddison_population.csv")
# primary_education_per_country = pd.read_csv("./data/education_baro_lee/primary_education.csv")
# secondary_education_per_country = pd.read_csv("./data/education_baro_lee/secondary_education.csv")
tertiary_education_per_country = pd.read_csv(
    "../data/education_baro_lee/er_tertiary_enrollment_rate_by_country_and_year.csv")

# --- calculate the amount of people with tertiary education per country


# Interpolate tertiary education data to make it yearly

# Prepare dataframes for interpolation
# For the tertiary education dataframe, melt it to long format for easier manipulation
tertiary_long = tertiary_education_per_country.melt(id_vars=["Country"], var_name="Year", value_name="Rate")
tertiary_long["Year"] = tertiary_long["Year"].astype(float)  # Ensure year is float for interpolation


# Function to interpolate for each country
def interpolate_country(df, year_range):
    interp_func = interp1d(df["Year"], df["Rate"], kind='linear', bounds_error=False, fill_value="extrapolate")
    return pd.Series(interp_func(year_range), index=year_range)


# Years to interpolate over, based on the population dataset's years
year_range = np.arange(1820, 2019)  # Till 2018, inclusive

# Apply interpolation for each country in the tertiary education dataset
interpolated_rates = tertiary_long.groupby("Country").apply(lambda x: interpolate_country(x, year_range)).unstack()

# Transpose to make years the columns again and reset index
interpolated_rates = interpolated_rates.transpose().reset_index()

# Rename columns for merging
interpolated_rates.columns = ["Year"] + list(interpolated_rates.columns[1:])

# Now, interpolate population data to ensure every year is present (if needed)
# However, based on initial inspection, it seems the population data may already be in an annual format
# Let's verify if interpolation is necessary by checking the year columns

# Display the interpolated tertiary education rates structure
print(interpolated_rates.head())
# print(population_per_country.columns)


# Transform population data to long format
population_long = population_per_country.melt(id_vars=["country"], var_name="Year", value_name="Population")
population_long["Year"] = population_long["Year"].astype(int)  # Ensure year is integer for matching

# Merge the interpolated tertiary education rates with the population data
merged_data = pd.merge(population_long, interpolated_rates, left_on=["country", "Year"], right_on=["Country", "Year"])
merged_data["Population"] = merged_data["Population"] * 1000  # Convert population from thousands to individual count

#  ---- Calculate the amount of people with tertiary education
merged_data["People_with_Tertiary_Education"] = (merged_data["Population"] * merged_data[0] / 100).round()

# Display the merged data structure and a sample
merged_data = merged_data.drop(columns=[0, 'Country'])  # Drop redundant column
print(merged_data.head())

# select countries I need
selected_countries = ['United States', 'China', 'India', 'Germany', 'United Kingdom', 'France', 'Brazil', 'Italy',
                      'Canada', 'South Korea', "Russian Federation"]

# select the data for the selected countries
selected_data = merged_data[merged_data['country'].isin(selected_countries)]
print(selected_data.head())
