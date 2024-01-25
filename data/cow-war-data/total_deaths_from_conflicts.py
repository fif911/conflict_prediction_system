import numpy as np
import pandas as pd

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

# print unique WarType for each dataset
print(ds1['WarType'].unique())
print(ds2['WarType'].unique())
print(ds3['WarType'].unique())

# get the list of conflicts for the countries of interest
# USA, United Kingdom, Germany, France, Russia, China, Ottoman Empire, Netherlands, Spain
CODES = [2, 200, 255, 220, 230, 365, 640, 210, 220]

# get the list of conflicts for ccode1 or ccode2 = 2

# ds1_usa = ds1[(ds1['ccode1'] == 2) | (ds1['ccode2'] == 2)]
# ds2_usa = ds2[(ds2['ccode'] == 2)]
# ds3_usa = ds3[(ds3['CcodeA'] == 2) | (ds3['CcodeB'] == 2)]
# ds4_usa = ds4[(ds4['ccode1'] == 2) | (ds4['ccode2'] == 2)]

print("Done")

# plot total battle deaths from ds1, ds2 and ds3 per year
# swap -8 with 0
ds1['BatDeath'] = ds1['BatDeath'].replace(-8, np.NAN)
ds1['NonStateDeaths'] = ds1['NonStateDeaths'].replace(-8, np.NAN)

ds2['BatDeath'] = ds2['BatDeath'].replace(-8, np.NAN)

# for values that have commas - remove the commas and convert to int
ds3['SideADeaths'] = ds3['SideADeaths'].str.replace(',', '').astype(float)
ds3['SideBDeaths'] = ds3['SideBDeaths'].str.replace(',', '').astype(float)

ds3['SideADeaths'] = ds3['SideADeaths'].replace(-8, np.NAN)
ds3['SideBDeaths'] = ds3['SideBDeaths'].replace(-8, np.NAN)
ds3['SideADeaths'] = ds3['SideADeaths'].replace(-9, np.NAN)
ds3['SideBDeaths'] = ds3['SideBDeaths'].replace(-9, np.NAN)


# for each year, sum the battle deaths
ds1_battle_deaths = ds1.groupby('StartYear1')['BatDeath'].sum()
ds1_nonstate_deaths = ds1.groupby('StartYear1')['NonStateDeaths'].sum()
ds2_battle_deaths = ds2.groupby('StartYear1')['BatDeath'].sum()
ds3_sideA_deaths = ds3.groupby('StartYear1')['SideADeaths'].sum()
ds3_sideB_deaths = ds3.groupby('StartYear1')['SideBDeaths'].sum()

# sum the battle deaths for each year for ds1_battle_deaths and ds1_nonstate_deaths
ds1_total_death = ds1_battle_deaths + ds1_nonstate_deaths
ds2_total_death = ds2_battle_deaths
ds3_total_death = ds3_sideA_deaths + ds3_sideB_deaths

# convert ds1_total_death float series to integers
ds1_total_death = ds1_total_death.astype(int)
ds2_total_death = ds2_total_death.astype(int)
ds3_total_death = ds3_total_death.astype(int)

# add the total deaths from all datasets for each year. In case of missing values, the sum is the sum of the non-missing values

total_deaths = ds1_total_death.add(ds2_total_death, fill_value=0)
total_deaths = total_deaths.add(ds3_total_death, fill_value=0)

# make 15 year maximum
total_deaths_rolling = total_deaths.rolling(5).max()

# plot the total battle deaths per year
# plot y scale without scientific notation

import matplotlib.pyplot as plt

plt.plot(total_deaths_rolling, label='Total')
plt.xlabel('Year')
plt.ylabel('Total Battle Deaths')
plt.title('Total Battle Deaths per Year')
plt.ticklabel_format(style='plain')
plt.legend()
plt.show()
