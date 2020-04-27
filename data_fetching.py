import pandas as pd
import numpy as np
import json
import wget
import os
import shutil

confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
# recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"

file = wget.download(confirmed_url, './c.csv')
if os.path.exists('./c.csv'):
    shutil.move(file, './c.csv')

file = wget.download(deaths_url, './d.csv')
if os.path.exists('./d.csv'):
    shutil.move(file, './d.csv')

# file = wget.download(recovered_url, './r.csv')
# if os.path.exists('./r.csv'):
#     shutil.move(file, './r.csv')

df_c = pd.read_csv('./c.csv', delimiter=',', keep_default_na=False)
df_d = pd.read_csv('./d.csv', delimiter=',', keep_default_na=False)
# df_r = pd.read_csv('./r.csv', delimiter=',', keep_default_na=False)

data = []
list_data = []
list_data_dict = {}

for index, row in df_c.iterrows():
    row_d = df_d.loc[index, :]
    # row_r = df_r.loc[index, :]
    d_item = {}

    # if (row['Province_State'] == ''):
    #     d_item['area'] = row['Country/Region']
    # else:
    #     d_item['area'] = row['Province/State'] + ', ' + row['Country/Region']
    d_item['area'] = row['Combined_Key']
    d_item['lat'] = row['Lat']
    d_item['lng'] = row['Long_']
    d_item['confirmed'] = int(row[df_c.columns[-1]])
    d_item['deaths'] = int(row_d[df_c.columns[-1]])

    county = row['Province_State']
    if county not in list_data_dict:
        list_data_dict[county] = {'confirmed': int(
            row[df_c.columns[-1]]), 'deaths': int(row_d[df_c.columns[-1]])}
    else:
        list_data_dict[county]['confirmed'] += int(row[df_c.columns[-1]])
        list_data_dict[county]['deaths'] += int(row_d[df_c.columns[-1]])

    d_item['date'] = df_c.columns[-1]
    data.append(d_item)

for key, value in list_data_dict.items():
    temp = {'state': key,
            'confirmed': value['confirmed'], 'deaths': value['deaths']}
    list_data.append(temp)

with open('./data.json', 'w') as f:
    json.dump(data, f)

with open('./list_data.json', 'w') as f:
    json.dump(list_data, f)
