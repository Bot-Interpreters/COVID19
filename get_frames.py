import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams

plt.style.use('seaborn')
rcParams.update({'figure.autolayout': True})

with open('data\\states_daily.json') as f:
    data = json.load(f)

confirmed_df = pd.DataFrame(data['confirmed'])
recovered_df = pd.DataFrame(data['recovered'])
deceased_df = pd.DataFrame(data['deceased'])
