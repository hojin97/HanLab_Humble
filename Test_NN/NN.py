import numpy as np
import tensorflow as tf
from tensorflow import keras

import os

config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.4
session = tf.compat.v1.InteractiveSession(config=config)

base_path = '../Humble/Data/resultVecs/resultVecs_20/'

X_i = []
y = []

for label in ['Bi', 'Tri']:
    for feature in ['striping']:
        for top, dir, f in os.walk(base_path + label + '/' + feature + '/'):
            for filename in f:
                data = open(os.path.join(base_path + label + '/' + feature + '/', filename), 'r')
                data = data.read()
                temp_data = []
                for d in data.split():
                    temp_data.append(float(d))
                X_i.append(temp_data.copy())

                if label == 'Bi':
                    y.append(2)
                else:
                    y.append(3)

print(len(X_i[0]))

X = np.array(X_i)
y = np.array(y)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# validation split

X_train, X_validation, y_train, y_validation = train_test_split(X_train, y_train, test_size=0.1, random_state=10, stratify=y_train)

# Hidden nodes
# input => 144
# output => 1
# training sample => (2400) 1920, (120) 96
# 1920 * 1 * (144 + 1) => 278,400

Neural_Network = keras.models.Sequential([
    # input layer
    keras.layers.Dense(1024, activation='relu', input_shape=(144,)),

    # hidden layer 1
    keras.layers.Dense(1024, activation='relu'),

    # hidden layer 2
    keras.layers.Dense(1024, activation='relu'),

    # output layer
    keras.layers.Dense(1, activation='sigmoid')
])

Neural_Network.summary()

Neural_Network.compile(loss=keras.losses.mean_squared_error, optimizer='rmsprop', metrics=['accuracy'])

Neural_Network.fit(X_train, y_train, epochs=10, batch_size=16)

evaluation = Neural_Network.evaluate(X_test, y_test, batch_size=16)
