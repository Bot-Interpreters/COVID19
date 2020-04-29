import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from tqdm import tqdm

plt.style.use('seaborn')
rcParams.update({'figure.autolayout': True})


def preprocess_df(df):
    df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
    df.index = df['date']
    df.drop(['date', 'status'], inplace=True, axis=1)

    for col in df:
        df[col] = pd.to_numeric(df[col])


def plot_daily_data(df, state, type_):

    fig = sns.barplot(df.index, df[state])
    fig.set_title(f'{type_} Cases ({state})')
    fig.set_ylabel('Number of Cases')

    fig.set_xticklabels(fig.get_xticklabels(),
                        rotation=45,
                        horizontalalignment='right',
                        fontweight='light')

    plt.gca().xaxis.set_major_formatter(plt.FixedFormatter(df.index.to_series().dt.strftime('%d %b %Y')))


def plot_cumulative_data(df, state, type_):
    if type_ == 'Confirmed':
        c = 'r'
    elif type_ == 'Recovered':
        c = 'g'
    elif type_ == 'Deceased':
        c = 'k'
    plt.plot(df.index, df[state], '--o', color=c, alpha=0.7)
    plt.title(f'{type_} Cases (Cumulative - {state})')
    plt.ylabel('Number of Cases')


with open('data\\states_daily.json') as f:
    data = json.load(f)

confirmed_df = pd.DataFrame(data['confirmed'])
recovered_df = pd.DataFrame(data['recovered'])
deceased_df = pd.DataFrame(data['deceased'])

preprocess_df(confirmed_df)
preprocess_df(recovered_df)
preprocess_df(deceased_df)

cum_confirmed_df = confirmed_df.cumsum()
cum_recovered_df = recovered_df.cumsum()
cum_deceased_df = deceased_df.cumsum()


def plot_data_state(state):

    plt.figure(figsize=(14, 15), dpi=100)

    plt.subplot(311)
    plot_daily_data(confirmed_df, state, 'Confirmed')

    plt.subplot(312)
    plot_daily_data(recovered_df, state, 'Recovered')

    plt.subplot(313)
    plot_daily_data(deceased_df, state, 'Deceased')

    plt.savefig(f'data_insight\\{state}_daily_cases.png')
    # plt.show()
    plt.close()

    plt.figure(figsize=(14, 15), dpi=100)

    plt.subplot(311)
    plot_cumulative_data(cum_confirmed_df, state, 'Confirmed')
    plt.subplot(312)
    plot_cumulative_data(cum_recovered_df, state, 'Recovered')
    plt.subplot(313)
    plot_cumulative_data(cum_deceased_df, state, 'Deceased')
    plt.savefig(f'data_insight\\{state}_cumulative.png')
    # plt.show()
    plt.close()
    print(f'[INFO] Plot saved for state: {state}')


for state in tqdm(sorted(data['confirmed'][0].keys())):
    if state != 'date' and state != 'status':
        plot_data_state(state)

print('[INFO] Plotted Data')
input("Press ENTER to exit...")
