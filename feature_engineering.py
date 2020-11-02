import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

df = pd.read_csv('taxi_train.csv', parse_dates=['pickup_datetime'], nrows=100000)

df = df[(df['fare_amount']>0) & (df['fare_amount']<100)]

df.loc[df['passenger_count']==0, 'passenger_count'] = 1

nyc_min_latitude = 40.63
nyc_max_latitude = 40.85
nyc_min_longitude = -74.05
nyc_max_longitude = -73.75


for long in ['pickup_longitude', 'dropoff_longitude']:
    df = df[(df[long] > nyc_min_longitude) & (df[long] < nyc_max_longitude)]

for lat in ['pickup_latitude', 'dropoff_latitude'] :
    df = df[(df[lat] > nyc_min_latitude) & (df[lat] < nyc_max_latitude)]


df['year'] = df['pickup_datetime'].dt.year
df['month'] = df['pickup_datetime'].dt.month
df['day'] = df['pickup_datetime'].dt.day
df['day_of_week'] = df['pickup_datetime'].dt.dayofweek
df['hour'] = df['pickup_datetime'].dt.hour


# print(df.loc[:5, ['pickup_datetime', 'year', 'month', 'day', 'day_of_week', 'hour' ]])

df.drop(['pickup_datetime'], axis=1)

def euc_distance(lat1, long1, lat2, long2):
    return ((lat1-lat2)**2 + (long1-long2)**2)**0.5

df['distance'] = euc_distance(df['pickup_latitude'],
                              df['pickup_longitude'],
                              df['dropoff_latitude'],
                              df['dropoff_longitude'])

df.plot.scatter('fare_amount', 'distance')
# plt.show()

airports = {'JFKairport':(-73.78, 40.643),
            'Laguardia airport':(73.87, 40.77),
            'Newark airport':(-74.18, 40.69)}

print(df['pickup_longitude'].shape)

for airport in airports:
    df['pickup_dist ' + airport] = euc_distance(df['pickup_latitude'], df['pickup_longitude'], airports[airport][1], airports[airport][0])

for airport in airports:
    df['dropoff_dist ' + airport] = euc_distance(df['dropoff_latitude'], df['dropoff_longitude'], airports[airport][1], airports[airport][0])

df = df.drop(['key'], axis=1)