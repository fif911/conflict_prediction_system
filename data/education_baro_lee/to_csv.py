import pandas as pd

if __name__ == '__main__':
    # Load the Excel file
    file_path = 'LeeLee_HC_MF1564.xls'  # Replace with your file path
    data_with_headers = pd.read_excel(file_path, skiprows=12)

    # Handling the "Country" column which has NaN values
    # Forward fill the NaN values in the 'Country' column ('Unnamed: 0')
    data_with_headers['Unnamed: 0'].fillna(method='ffill', inplace=True)


    def read_and_save(column, new_column_name):
        data_cleaned = data_with_headers[['Unnamed: 0', 'Unnamed: 1', column]]
        data_cleaned.columns = ['Country', 'Year', new_column_name]

        # Remove rows with NaN values
        data_cleaned.dropna(inplace=True)

        # Transform the data to have countries as rows, years as columns, and human capital values as cell values
        data_pivoted = data_cleaned.pivot(index='Country', columns='Year', values=new_column_name)

        # Save the transformed data to a CSV file
        csv_file_path = f'{new_column_name.lower().replace(" ", "_")}_by_country_and_year.csv'  # Replace with your desired file path
        data_pivoted.to_csv(csv_file_path)


    read_and_save('Unnamed: 4', 'Human Capital')
    print("Done")
