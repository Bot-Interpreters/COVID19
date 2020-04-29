import requests
import json

raw_data_url = "https://raw.githubusercontent.com/covid19india/api/gh-pages/csv/latest/raw_data.csv"
states_daily_url = "https://api.covid19india.org/states_daily.json"
time_series_url = "https://api.covid19india.org/data.json"

data = requests.get(raw_data_url, allow_redirects=True)
with open('data\\raw_data.csv', 'wb') as f:
    f.write(data.content)

print('[INFO] Collected raw_data.csv')

data = requests.get(states_daily_url, allow_redirects=True)
with open('data\\states_daily.json', 'wb') as f:
    f.write(data.content)

print('[INFO] Collected states_daily.json')

data = requests.get(time_series_url, allow_redirects=True)
with open('data\\time_series.json', 'wb') as f:
    f.write(data.content)

print('[INFO] Collected time_series.json')

with open('data\\states_daily.json') as f:
    data = json.load(f)

data = data['states_daily']

custom_data = {
    'confirmed': [],
    'deceased': [],
    'recovered': [],
}

for frame in data:
    if frame['status'] == 'Confirmed':
        custom_data['confirmed'].append(frame)
    elif frame['status'] == 'Deceased':
        custom_data['deceased'].append(frame)
    elif frame['status'] == 'Recovered':
        custom_data['recovered'].append(frame)
    else:
        raise ValueError(f'\n[ERROR] \n{frame}\n')

with open('data\\states_daily.json', 'w') as f:
    json.dump(custom_data, f, indent=4)

print('[INFO] Preprocessed states_daily.json')
input('Press ENTER to quit...')
