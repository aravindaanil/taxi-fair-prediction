import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

df = pd.read_csv('taxi_train.csv', parse_dates=['pickup_datetime'], nrows=100000)

df['year'] = df['pickup_datetime'].dt.year
df['month'] = df['pickup_datetime'].dt.month
df['day'] = df['pickup_datetime'].dt.day
df['day_of_week'] = df['pickup_datetime'].dt.dayofweek
df['hour'] = df['pickup_datetime'].dt.hour



df['hour'].plot.hist(bins=24, ec='black')

plt.title('Pickup hour Histogram')
plt.xlabel('Hour ')
plt.show()


