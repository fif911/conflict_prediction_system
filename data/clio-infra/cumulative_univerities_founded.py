import pandas as pd

# Load the data from the Excel file
file_path = './UniversitiesFounded_Broad (1).xlsx'
data = pd.read_excel(file_path)

# Display the first few rows of the dataframe to understand its structure
data.head()
# Replace NaNs with 0s for calculation
data_filled = data.fillna(0)

# Perform cumulative sum horizontally, starting from the first year column
cumulative_universities = data_filled.iloc[:, 3:].cumsum(axis=1)

# Combine the cumulative data back with the country information
cumulative_universities_data = pd.concat([data_filled.iloc[:, :3], cumulative_universities], axis=1)

# Show the first few rows of the transformed dataframe
print(cumulative_universities_data.head())

# remove all years after 2015
cumulative_universities_data = cumulative_universities_data.loc[:, :'2015']
# save the data to a csv file
cumulative_universities_data.to_csv('cumulative_universities_founded.csv', index=False)
