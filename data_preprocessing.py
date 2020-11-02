import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

df = pd.read_csv('taxi_train.csv', parse_dates=['pickup_datetime'], nrows=100000)

print(df.isnull().sum())
print(df.describe())

df['fare_amount'].plot.hist(bins=500, ec='black')
plt.xlabel('Fare')
plt.title('Histogram of fares')
plt.show()

print(max(df['passenger_count']))

df = df[(df['fare_amount']>0) & (df['fare_amount']<100)]

df['passenger_count'].plot.hist(bins=6, ec='black')
plt.xlabel('passenger count')
plt.title('Histogram of passenger count')
plt.show()

df.loc[df['passenger_count']==0, 'passenger_count'] = 1

df.plot.scatter('pickup_latitude', 'pickup_longitude')
plt.show()

nyc_min_longitude = -74.05
nyc_max_longitude = -73.75

nyc_min_latitude = 40.63
nyc_max_latitude = 40.85


for long in ['pickup_longitude', 'dropoff_longitude']:
    df = df[(df[long] > nyc_min_longitude) & (df[long] < nyc_max_longitude)]

for lat in ['pickup_latitude', 'dropoff_latitude'] :
    df = df[(df[lat] > nyc_min_latitude) & (df[lat] < nyc_max_latitude)]
