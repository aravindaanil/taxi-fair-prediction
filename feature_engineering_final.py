import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense


def feature_engineer(df):
    def create_time_features(df):
        df['year'] = df['pickup_datetime'].dt.year
        df['month'] = df['pickup_datetime'].dt.month
        df['day'] = df['pickup_datetime'].dt.day
        df['day_of_week'] = df['pickup_datetime'].dt.dayofweek
        df['hour'] = df['pickup_datetime'].dt.hour
        df = df.drop(['pickup_datetime'], axis=1)
        return df

    def euc_distance(lat1, long1, lat2, long2):
        return ((lat1-lat2)**2 + (long1-long2)**2)**0.5

    def create_pickup_dropoff_dist_features(df):
        df['travel_distance'] = euc_distance(df['pickup_latitude'], df['pickup_longitude'], df['dropoff_latitude'], df['dropoff_longitude'] )
        return df

    def create_airport_distant_features(df):
        airports = {'JFKairport': (-73.78, 40.643),
                    'Laguardia airport': (73.87, 40.77),
                    'Newark airport': (-74.18, 40.69)}
        for k in airports:
            df['pickup_dist_' + k] = euc_distance(df['pickup_latitude'], df['pickup_longitude'], airports[k][1], airports[k][0] )

            df['dropoff_dist_' + k] = euc_distance(df['dropoff_latitude'], df['dropoff_longitude'], airports[k][1],
                                                  airports[k][0])
            return df

    df = create_time_features(df)
    df = create_pickup_dropoff_dist_features(df)
    df = create_airport_distant_features(df)
    df = df.drop(['key'], axis=1)
    return df








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


df = feature_engineer(df)

# print(df.head())

df_prescaled = df.copy()
df_scaled = df.drop(['fare_amount'], axis=1)
print(type(df))


df_scaled = scale(df_scaled)

cols = df.columns.tolist()
cols.remove('fare_amount')
df_scaled = pd.DataFrame(df_scaled, columns=cols, index=df.index)
df_scaled = pd.concat([df_scaled, df['fare_amount']], axis=1)
df = df_scaled.copy()


X = df.loc[:, df.columns!='fare_amount']
y = df.loc[:, 'fare_amount']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


model = Sequential()
model.add(Dense(128, activation='relu', input_dim=X_train.shape[1]))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1))

model.summary()


sample = X_test.sample(n=1, random_state=np.random.randint(low=0, high=10000))
idx = sample.index[0]

day_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

print(df_prescaled.loc[idx, 'hour'])



