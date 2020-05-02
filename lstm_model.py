import json
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam

plt.style.use('seaborn')


def get_data():

    with open('data\\states_daily.json') as f:
        data = json.load(f)

    confirmed_df = pd.DataFrame(data['confirmed'])
    confirmed_df['date'] = pd.to_datetime(confirmed_df['date'], infer_datetime_format=True)
    confirmed_df.index = confirmed_df['date']
    confirmed_df.drop(['date', 'status'], inplace=True, axis=1)

    for col in confirmed_df:
        confirmed_df[col] = pd.to_numeric(confirmed_df[col])

    data = confirmed_df['tn'].values

    return data


def get_timeseries_data(data, window=5):
    time_series_data = []

    for i in range(len(data) - window):
        time_series_data.append([data[i:i + window], data[i + window]])

    np.random.shuffle(time_series_data)

    X = []
    y = []

    for x_, y_ in time_series_data:
        X.append(x_)
        y.append(y_)

    return np.array(X), np.array(y)


def get_model(lstm_units=[32],
              dense_units=[16],
              window=5,
              n_features=1,
              name='Sequential_model'):

    model = Sequential(name=name)
    model.add(Input(shape=(window, n_features)))

    for i in range(len(lstm_units)):
        if i == len(lstm_units) - 1:
            model.add(LSTM(lstm_units[i], return_sequences=False))
        else:
            model.add(LSTM(lstm_units[i], return_sequences=True))

    if dense_units:
        for i in range(len(dense_units)):
            model.add(Dense(dense_units[i], activation='relu'))

    model.add(Dense(1))

    return model


data = get_data()
train, test = train_test_split(data.reshape(-1, 1), test_size=0.2, shuffle=False)

train_x, train_y = get_timeseries_data(train)
test_x, test_y = get_timeseries_data(test)

scalar = StandardScaler()
scalar.fit(train_x.reshape(-1, 1))
train_x = scalar.transform(train_x.reshape(-1, 1)).reshape(-1, 5, 1)
test_x = scalar.transform(test_x.reshape(-1, 1)).reshape(-1, 5, 1)

print(f'Shape of train_x :{train_x.shape}')
print(f'Shape of train_y :{train_y.shape}')
print(f'Shape of test_x :{test_x.shape}')
print(f'Shape of test_y :{test_y.shape}')

model = get_model(lstm_units=[16, 32], dense_units=[16])

model.compile(loss='mae', optimizer=Adam(lr=1e-3, decay=1e-5))
model.summary()

es = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

history = model.fit(train_x, train_y, batch_size=16, epochs=1000,
                    validation_data=(test_x, test_y), verbose=0,
                    callbacks=[es])

train_mae = model.evaluate(train_x, train_y, verbose=0)
test_mae = model.evaluate(test_x, test_y, verbose=0)

print(f'\nTrain MAE: {train_mae:.3f}')
print(f'Test MAE: {test_mae:.3f}\n')

train_pred = model.predict(train_x)
test_pred = model.predict(test_x)

# train_y = scalar.inverse_transform(train_y)
# train_pred = scalar.inverse_transform(train_pred)
# test_y = scalar.inverse_transform(test_y)
# test_pred = scalar.inverse_transform(test_pred)

plt.plot(history.history['loss'], label='Train Loss MAE')
plt.plot(history.history['val_loss'], label='Test Loss MAE')
plt.xlabel('Epochs')
plt.ylabel('MAE')
plt.legend()
plt.show()
plt.close()

plt.figure(figsize=(12, 7))

plt.subplot(211)
plt.plot(train_y, '--o', label='Truth')
plt.plot(train_pred, '--o', label='Pred')
plt.title('Train Data')
plt.legend()

plt.subplot(212)
plt.plot(test_y, '--o', label='Truth')
plt.plot(test_pred, '--o', label='Pred')
plt.title('Test Data')
plt.legend()

plt.show()
plt.close()
