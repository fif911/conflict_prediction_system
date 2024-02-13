import pandas as pd

file_path = 'LeeLee_HC_MF1564.xls'
# file_path = 'LeeLee_enroll_MF.xls'

if __name__ == '__main__':
    # Load the Excel file

    MODE = 'HC'  # Human Capital
    skiprows = 13
    if 'enroll' in file_path:
        MODE = 'ER'  # Enrollment Rate
        skiprows = 10
    data_with_headers = pd.read_excel(file_path, skiprows=skiprows)

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
        csv_file_path = f'{MODE.lower()}_{new_column_name.lower().replace(" ", "_")}_by_country_and_year_{int(min(data_cleaned["Year"]))}_{int(max(data_cleaned["Year"]))}.csv'
        if new_column_name == 'Population':
            # multiply by 1000 to get the actual population
            data_pivoted = data_pivoted * 1000
            data_pivoted.to_csv(csv_file_path, float_format='%.f')
        data_pivoted.to_csv(csv_file_path)


    if MODE == 'HC':
        read_and_save('Unnamed: 4', 'Human Capital')
        read_and_save('Unnamed: 5', 'Alternative Human Capital')
        read_and_save('Unnamed: 6', 'Population')
    elif MODE == 'ER':
        read_and_save('Unnamed: 2', 'Primary Enrollment Rate')
        read_and_save('Unnamed: 3', 'Secondary Enrollment Rate')
        read_and_save('Unnamed: 4', 'Tertiary Enrollment Rate')
    else:
        raise ValueError(f'Invalid mode: {MODE}')

    print("Done")
