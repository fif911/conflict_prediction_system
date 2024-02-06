# Modified script to read Maddison's 'Full data' sheet and save it to a CSV file
import pandas as pd


# Define a function to process and save the 'Full data' sheet to CSV
def save_maddison_data_to_csv(excel_path, sheet_name, csv_file_path):
    # Read the specified sheet from the Excel file
    data_df = pd.read_excel(excel_path, sheet_name=sheet_name)

    # Optional: Handle NaN values if necessary (e.g., drop rows with NaN in 'gdppc' and 'pop')
    # For demonstration, we'll keep all rows to preserve the dataset's integrity, including those with NaN values.

    # Save the data to a CSV file
    data_df.to_csv(csv_file_path, index=False)

    return csv_file_path


maddison_excel_path = './mpd2020.xlsx'
csv_output_path = './maddison_full_data.csv'

# Call the function to process and save the Maddison data to CSV
saved_csv_path = save_maddison_data_to_csv(maddison_excel_path, 'Full data', csv_output_path)


def create_pivot_csvs_from_maddison_data(excel_path, sheet_name, gdp_csv_path, pop_csv_path):
    # Read the specified sheet from the Excel file
    data_df = pd.read_excel(excel_path, sheet_name=sheet_name)

    # Filter the data to include only the years 1820 to 2018
    data_filtered = data_df[data_df['year'].between(1820, 2018)]

    # Create pivot tables for GDP per capita and population
    gdp_pivot = data_filtered.pivot(index='country', columns='year', values='gdppc')
    pop_pivot = data_filtered.pivot(index='country', columns='year', values='pop')

    # Save the pivot tables to CSV files
    gdp_pivot.to_csv(gdp_csv_path)
    pop_pivot.to_csv(pop_csv_path)

    return gdp_csv_path, pop_csv_path


# Specify the CSV file paths where the data will be saved
gdp_csv_output_path = './maddison_gdp_per_capita.csv'
pop_csv_output_path = './maddison_population.csv'

# Call the function to process the data and create the pivot CSV files
gdp_csv_path, pop_csv_path = create_pivot_csvs_from_maddison_data(
    maddison_excel_path, 'Full data', gdp_csv_output_path, pop_csv_output_path
)
