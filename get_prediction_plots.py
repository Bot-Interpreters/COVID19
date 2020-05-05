import json
import datetime
import pandas as pd
import pmdarima as pm
import matplotlib.pyplot as plt

plt.style.use('seaborn')

with open('data\\states_daily.json') as f:
    data = json.load(f)

confirmed_df = pd.DataFrame(data['confirmed'])
confirmed_df['date'] = pd.to_datetime(confirmed_df['date'], infer_datetime_format=True)
confirmed_df.index = confirmed_df['date']
confirmed_df.drop(['date', 'status'], inplace=True, axis=1)

for col in confirmed_df:
    confirmed_df[col] = pd.to_numeric(confirmed_df[col])


def arima_fit_predict_plot(state='tn', cum=False, future_days=7):

    if not cum:
        series = confirmed_df[state]
    else:
        series = confirmed_df[state].cumsum()

    arima_model = pm.auto_arima(series,
                                trace=False,
                                suppress_warnings=True,
                                error_action='ignore')

    predictions = arima_model.predict(n_periods=future_days)
    dates = [series.index[-1] + datetime.timedelta(days=i) for i in range(1, future_days + 1)]

    plt.plot(series, '--o', label='History')
    plt.plot(dates, predictions, '--o', label='Predictions')
    plt.title(f'ARIMA Prediction: {state.upper()} Cumulative - {cum}')
    plt.legend()
    plt.tight_layout()
    plt.show()


arima_fit_predict_plot(state='tn', cum=False)
arima_fit_predict_plot(state='tn', cum=True)
arima_fit_predict_plot(state='tt', cum=False)
arima_fit_predict_plot(state='tt', cum=True)

while True:
    ui = input("Enter state code, 'q' to quit: ")
    if ui == 'q':
        break

    arima_fit_predict_plot(state=ui, cum=False)
    arima_fit_predict_plot(state=ui, cum=True)
