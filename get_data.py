import requests

raw_data_url = "https://raw.githubusercontent.com/covid19india/api/gh-pages/csv/latest/raw_data.csv"
states_daily_url = "https://api.covid19india.org/states_daily.json"
time_series_url = "https://api.covid19india.org/data.json"

data = requests.get(raw_data_url, allow_redirects=True)
with open('data\\raw_data.csv', 'wb') as f:
    f.write(data.content)

data = requests.get(states_daily_url, allow_redirects=True)
with open('data\\states_daily.json', 'wb') as f:
    f.write(data.content)

data = requests.get(time_series_url, allow_redirects=True)
with open('data\\time_series.json', 'wb') as f:
    f.write(data.content)
