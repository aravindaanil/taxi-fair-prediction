from keras.models import Sequential
from keras.layers import Dense
#print(tf.__version__)
model = Sequential()
#model = tf.keras.Sequential()
# model.add(Dense(8, input_shape=(16,)))

model.add(Dense(128, activation='relu', input_shape=(16,)))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1))

print(model.summary())