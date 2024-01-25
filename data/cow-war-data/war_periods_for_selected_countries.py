"""Conflict periods for selected countries by type of conflict"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker


# get the list of conflicts for the countries of interest and plot by type of the conflict
# USA, United Kingdom, Germany, France, Russia, China, Turkey, Netherlands, Spain
CODES = [2, 200, 255, 220, 365, 710, 640, 210, 230]
COUNTRIES = ['USA', 'United Kingdom', 'Germany', 'France', 'Russia', 'China', 'Turkey', 'Netherlands', 'Spain']
CASUALTIES_THRESHOLD = 50_000  # how major conflict should be to be considered


# for Germany there are:
# Germany
# German Federal Republic
# German Democratic Republic
# Baden
# Saxony
# Wuerttemburg
# Hesse Electoral
# Hesse Grand Ducal
# Mecklenburg Schwerin
# Bavaria

def convert_to_int(ds1, ds2, ds3):
    # swap -8 with 0
    ds1['BatDeath'] = ds1['BatDeath'].replace(-8, np.NAN)
    ds1['NonStateDeaths'] = ds1['NonStateDeaths'].replace(-8, np.NAN)

    ds2['BatDeath'] = ds2['BatDeath'].replace(-8, np.NAN)

    # for values that have commas - remove the commas and convert to int
    ds3['SideADeaths'] = ds3['SideADeaths'].str.replace(',', '')
    ds3['SideBDeaths'] = ds3['SideBDeaths'].str.replace(',', '')

    ds3['SideADeaths'] = ds3['SideADeaths'].replace(-8, np.NAN)
    ds3['SideBDeaths'] = ds3['SideBDeaths'].replace(-8, np.NAN)
    ds3['SideADeaths'] = ds3['SideADeaths'].replace(-9, np.NAN)
    ds3['SideBDeaths'] = ds3['SideBDeaths'].replace(-9, np.NAN)

    return ds1, ds2, ds3


def get_major_conflicts_periods(ds1: pd.DataFrame, ds2: pd.DataFrame, ds3: pd.DataFrame):
    # convert columns to int or 0 if NaN
    ds1['BatDeath'] = ds1['BatDeath'].fillna(0).astype(int)
    ds1['NonStateDeaths'] = ds1['NonStateDeaths'].fillna(0).astype(int)
    ds2['BatDeath'] = ds2['BatDeath'].fillna(0).astype(int)
    ds3['SideADeaths'] = ds3['SideADeaths'].fillna(0).astype(int)
    ds3['SideBDeaths'] = ds3['SideBDeaths'].fillna(0).astype(int)

    conflicts_start_years = []
    conflicts_end_years = []

    for index, row in ds1.iterrows():
        start = row['StartYear1']
        end = row['EndYear1']
        if row['BatDeath'] + row['NonStateDeaths'] >= CASUALTIES_THRESHOLD:
            conflicts_start_years.append(start)
            conflicts_end_years.append(end)

    for index, row in ds2.iterrows():
        start = row['StartYear1']
        end = row['EndYear1']
        if row['BatDeath'] >= CASUALTIES_THRESHOLD:
            conflicts_start_years.append(start)
            conflicts_end_years.append(end)

    for index, row in ds3.iterrows():
        start = row['StartYear1']
        end = row['EndYear1']
        if row['SideADeaths'] + row['SideBDeaths'] >= CASUALTIES_THRESHOLD:
            conflicts_start_years.append(start)
            conflicts_end_years.append(end)

    return conflicts_start_years, conflicts_end_years


def get_conflict_series_by_type(war_type: int, ds1: pd.DataFrame, ds2: pd.DataFrame, ds3: pd.DataFrame,
                                casualties_threshold: int = 0):
    # for each conflict in ds1, ds2, ds3
    # get min start year and max end year for the country code
    # convert StartYear1 and EndYear1 to int

    ds1['StartYear1'] = ds1['StartYear1'].astype(int)
    ds1['EndYear1'] = ds1['EndYear1'].fillna(2008).astype(int)
    ds2['StartYear1'] = ds2['StartYear1'].astype(int)
    ds2['EndYear1'] = ds2['EndYear1'].fillna(2008).astype(int)
    ds3['StartYear1'] = ds3['StartYear1'].astype(int)
    ds3['EndYear1'] = ds3['EndYear1'].fillna(2008).astype(int)

    ds1['BatDeath'] = ds1['BatDeath'].fillna(0).astype(int)
    ds1['NonStateDeaths'] = ds1['NonStateDeaths'].fillna(0).astype(int)
    ds2['BatDeath'] = ds2['BatDeath'].fillna(0).astype(int)
    ds3['SideADeaths'] = ds3['SideADeaths'].fillna(0).astype(int)
    ds3['SideBDeaths'] = ds3['SideBDeaths'].fillna(0).astype(int)

    series_start = int(min(min(ds1['StartYear1']), min(ds2['StartYear1']),
                           min(ds3['StartYear1'])))
    series_end = int(max(max(ds1['EndYear1']), max(ds2['EndYear1']),
                         max(ds3['EndYear1'])))
    war_type_series = pd.Series(np.zeros(int(series_end - series_start)),
                                index=np.arange(series_start, series_end)).astype(int)

    if war_type == 2 or war_type == 3:
        for index, row in ds1.iterrows():
            # get the internal of the conflict in years (start and end)
            start = row['StartYear1']
            end = row['EndYear1']
            # if the conflict is of type 1, set the values in the series to 1
            total_conflict_casualties = int(row['BatDeath']) + int(row['NonStateDeaths'])
            if row['WarType'] == war_type and total_conflict_casualties >= casualties_threshold:
                war_type_series.loc[start:end] = 1

    elif war_type == 1:
        for index, row in ds2.iterrows():
            # get the internal of the conflict in years (start and end)
            start = row['StartYear1']
            end = row['EndYear1']
            # if the conflict is of type 1, set the values in the series to 1
            total_conflict_casualties = int(row['BatDeath'])
            if row['WarType'] == war_type and total_conflict_casualties >= casualties_threshold:
                war_type_series.loc[start:end] = 1

    elif war_type == 4 or war_type == 5 or war_type == 6 or war_type == 7:
        for index, row in ds3.iterrows():
            # get the internal of the conflict in years (start and end)
            start = row['StartYear1']
            end = row['EndYear1']
            # if the conflict is of type 1, set the values in the series to 1
            total_conflict_casualties = int(row['SideADeaths']) + int(row['SideBDeaths'])
            if row['WarType'] == war_type and total_conflict_casualties >= casualties_threshold:
                war_type_series.loc[start:end] = 1
    else:
        raise ValueError("Invalid war type")

    return war_type_series


if __name__ == '__main__':

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


    ds1, ds2, ds3 = convert_to_int(ds1, ds2, ds3)

    for ccode, cname in zip(CODES, COUNTRIES):
        ds1_country = ds1[(ds1['ccode1'] == ccode) | (ds1['ccode2'] == ccode)]
        ds2_country = ds2[(ds2['ccode'] == ccode)]
        ds3_country = ds3[(ds3['CcodeA'] == ccode) | (ds3['CcodeB'] == ccode)]

        # generate an ascending series similar to country GDP
        GDP = pd.Series(np.arange(1800, 2016), index=np.arange(1800, 2016))

        # ----- CONFLICTS BY TYPE 0 or 1 per year series -----
        # make an 8 series for each type of conflict based on each dataset
        # if in any dataset there is a conflict of that type in this year, set the value to 1
        # if not, set the value to 0
        # war_type_1 = pd.Series(np.zeros(216), index=np.arange(1800, 2016))
        # war_type_1 = get_conflict_series_by_type(1, ds1_country, ds2_country, ds3_country,
        #                                          casualties_threshold=CASUALTIES_THRESHOLD)
        # war_type_2 = get_conflict_series_by_type(2, ds1_country, ds2_country, ds3_country,
        #                                          casualties_threshold=CASUALTIES_THRESHOLD)
        # war_type_3 = get_conflict_series_by_type(3, ds1_country, ds2_country, ds3_country,
        #                                          casualties_threshold=CASUALTIES_THRESHOLD)
        # war_type_4 = get_conflict_series_by_type(4, ds1_country, ds2_country, ds3_country,
        #                                          casualties_threshold=CASUALTIES_THRESHOLD)
        # war_type_5 = get_conflict_series_by_type(5, ds1_country, ds2_country, ds3_country,
        #                                          casualties_threshold=CASUALTIES_THRESHOLD)
        # war_type_6 = get_conflict_series_by_type(6, ds1_country, ds2_country, ds3_country,
        #                                          casualties_threshold=CASUALTIES_THRESHOLD)
        # war_type_7 = get_conflict_series_by_type(7, ds1_country, ds2_country, ds3_country,
        #                                          casualties_threshold=CASUALTIES_THRESHOLD)

        # merge all war types into one series with 1 for each year there was a conflict of any type
        # war_type_all: pd.Series = war_type_1 + war_type_2 + war_type_3 + war_type_4 + war_type_5 + war_type_6 + war_type_7
        # if there was a conflict of any type in this year, set the value to 1
        # war_type_all = war_type_all.apply(lambda x: 1 if x > 0 else 0)

        # civil_wars_over_central_control_or_war_between_states = war_type_4 + war_type_1
        # civil_wars_over_central_control_or_war_between_states = civil_wars_over_central_control_or_war_between_states.apply(
        #     lambda x: 1 if x > 0 else 0)

        # bar_series = civil_wars_over_central_control_or_war_between_states  # changeable bar series
        #
        # plt.rcParams["figure.figsize"] = [7.50, 3.50]
        # plt.rcParams["figure.autolayout"] = True
        #
        # fig, ax = plt.subplots()
        #
        # bar_series = bar_series * GDP.max()
        # ax.bar(bar_series.index, bar_series.values, color='black', alpha=0.5)
        # ax.plot(GDP.index, GDP.values, color='red', ms=10)
        # # war_type_1.plot(kind='bar', color='black', alpha=0.5)
        # # GDP.plot(kind='line', color='red', ms=10)
        # plt.title(f'{cname} conflict periods and dummy GDP')
        # plt.xlabel('Year')
        # plt.ylabel('GDP')
        #
        # loc = plticker.MultipleLocator(base=25.0)
        # ax.xaxis.set_major_locator(loc)
        # plt.show()

        # ----- MAJOR CONFLICTS HIGHLIGHED -----
        start_years, end_years = get_major_conflicts_periods(ds1_country, ds2_country, ds3_country)

        fig, ax = plt.subplots()
        ax.plot(GDP.index, GDP.values, color='red', ms=10)
        for start, end in zip(start_years, end_years):
            ax.axvspan(start, end, alpha=0.5, color='black')
        plt.title(f'{cname} major conflict periods and dummy GDP')
        plt.show()
