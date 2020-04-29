import json
import datetime
import pandas as pd
import pmdarima as pm

with open('data\\states_daily.json') as f:
    data = json.load(f)

confirmed_df = pd.DataFrame(data['confirmed'])
confirmed_df['date'] = pd.to_datetime(confirmed_df['date'], infer_datetime_format=True)
confirmed_df.index = confirmed_df['date']
confirmed_df.drop(['date', 'status'], inplace=True, axis=1)

for col in confirmed_df:
    confirmed_df[col] = pd.to_numeric(confirmed_df[col])


def get_number_of_confirmed_cases(series, title='', future_days=3):

    arima_model = pm.auto_arima(series,
                                trace=False,
                                suppress_warnings=True,
                                error_action='ignore')

    predictions = arima_model.predict(n_periods=future_days)
    dates = [series.index[-1] + datetime.timedelta(days=i) for i in range(1, future_days + 1)]

    print(f'\nType of Prediction: {title}')

    for i in range(future_days):
        print(f"Date: {dates[i].strftime('%Y-%m-%d')} Prediction: {round(predictions[i])}")


def get_predictions(place='tn'):
    df = confirmed_df[place]
    df_cum = confirmed_df[place].cumsum()

    print(f'\nSample Size: {len(df)}')

    if place == 'tt':
        title = 'Total'
    else:
        title = place.upper()

    get_number_of_confirmed_cases(df, title=f'{title} Confirmed Cases')
    get_number_of_confirmed_cases(df_cum, title=f'{title} Confirmed Cases Cumulative')


get_predictions('tt')
get_predictions('tn')

while True:
    ui = input("\nEnter state code abbreviation, 'q' to quit: ")

    if ui == 'q':
        break

    get_predictions(ui)
