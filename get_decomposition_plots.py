import json
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

with open('data\\states_daily.json') as f:
    data = json.load(f)

confirmed_df = pd.DataFrame(data['confirmed'])
confirmed_df['date'] = pd.to_datetime(confirmed_df['date'], infer_datetime_format=True)
confirmed_df.index = confirmed_df['date']
confirmed_df.drop(['date', 'status'], inplace=True, axis=1)

for col in confirmed_df:
    confirmed_df[col] = pd.to_numeric(confirmed_df[col])


def get_seasonal_decompose(state='tn', cum=False):
    if cum:
        data = pd.DataFrame(confirmed_df[state].cumsum())
    else:
        data = pd.DataFrame(confirmed_df[state])

    result = seasonal_decompose(data, model='additive')
    fig = result.plot()
    plt.title(f'Seasonal Decompose - {state} Cumulative: {cum}')
    plt.show()


get_seasonal_decompose('tn')
get_seasonal_decompose('tn', True)
get_seasonal_decompose('tt')
get_seasonal_decompose('tt', True)

while True:
    ui = input("Enter state code, 'q' to quit: ")
    if ui == 'q':
        break

    get_seasonal_decompose(ui)
    get_seasonal_decompose(ui, True)
