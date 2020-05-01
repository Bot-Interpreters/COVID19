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


def get_predictions_rolling_average(series, title='', window=3):
    prediction_date = series.index[-1] + datetime.timedelta(days=1)
    total_cases_window = 0
    for i in range(1, window + 1):
        total_cases_window += series[-i]
    prediction_value = total_cases_window / window

    print(f'\nType of Prediction: {title}, Model: Rolling Average ({window} days)')
    print(f"Date: {prediction_date.strftime('%Y-%m-%d')} Prediction: {round(prediction_value)}")


def get_number_of_confirmed_cases_arima(series, title='', future_days=3):

    arima_model = pm.auto_arima(series,
                                trace=False,
                                suppress_warnings=True,
                                error_action='ignore')

    predictions = arima_model.predict(n_periods=future_days)
    dates = [series.index[-1] + datetime.timedelta(days=i) for i in range(1, future_days + 1)]

    print(f'\nType of Prediction: {title}, Model: ARIMA')

    for i in range(future_days):
        print(f"Date: {dates[i].strftime('%Y-%m-%d')} Prediction: {round(predictions[i])}")


def get_predictions_arima_and_rolling_average(place='tn'):
    df = confirmed_df[place]
    df_cum = confirmed_df[place].cumsum()

    print(f'\nSample Size: {len(df)}')

    if place == 'tt':
        title = 'Total'
    else:
        title = place.upper()

    get_number_of_confirmed_cases_arima(df, title=f'{title} Confirmed Cases')
    get_predictions_rolling_average(df, title=f'{title} Confirmed Cases')
    get_number_of_confirmed_cases_arima(df_cum, title=f'{title} Confirmed Cases Cumulative')
    get_predictions_rolling_average(df_cum, title=f'{title} Confirmed Cases Cumulative')


get_predictions_arima_and_rolling_average('tt')
get_predictions_arima_and_rolling_average('tn')

while True:
    ui = input("\nEnter state code abbreviation, 'q' to quit: ")

    if ui == 'q':
        break

    get_predictions_arima_and_rolling_average(ui)
