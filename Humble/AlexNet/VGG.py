import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = 0.4
session = InteractiveSession(config=config)

# 파일 불러오기
import os
import cv2

image_size = 227

groups_folder_path = '../Data/AAFT_5/'

X_r = []
y = []

for label in ['Bi', 'Tri']:

    for feature in ['stripe_bw']:

        for top, dir, f in os.walk(groups_folder_path + label + "/" + feature + "/"):
            for filename in f:
                img = cv2.imread(groups_folder_path + label + "/" + feature + "/" + filename)
                img = cv2.resize(img, None, fx=image_size / img.shape[0], fy=image_size / img.shape[1])

                X_r.append(img / 256)

                if label == 'Bi':
                    y.append(2)
                else:
                    y.append(3)

print(X_r[0].shape)

# CWT 의 경우 RMS 와 Angle을 2겹으로 진행

X = np.array(X_r)
y = np.array(y)

# train, test split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# validation split

X_train, X_validation, y_train, y_validation = train_test_split(X_train, y_train, test_size=0.1, random_state=10, stratify=y_train)

AlexNet = keras.models.Sequential([
    keras.layers.Conv2D(filters=64, kernel_size=(3,3), strides=1, padding="same", activation="relu", input_shape=(227, 227, 3)),
    keras.layers.Conv2D(filters=64, kernel_size=(3,3), strides=1, padding="same", activation="relu"),
    keras.layers.MaxPooling2D(pool_size=(2, 2), strides= 2),

    keras.layers.Conv2D(filters=128, kernel_size=(3,3), strides=1, padding="same", activation="relu"),
    keras.layers.Conv2D(filters=128, kernel_size=(3,3), strides=1, padding="same", activation="relu"),
    keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2),

    keras.layers.Conv2D(filters=256, kernel_size=(3,3), strides=1, padding="same", activation="relu"),
    keras.layers.Conv2D(filters=256, kernel_size=(3,3), strides=1, padding="same", activation="relu"),
    keras.layers.Conv2D(filters=256, kernel_size=(3,3), strides=1, padding="same", activation="relu"),
    keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2),

    keras.layers.Conv2D(filters=512, kernel_size=(3,3), strides=1, padding="same", activation="relu"),
    keras.layers.Conv2D(filters=512, kernel_size=(3,3), strides=1, padding="same", activation="relu"),
    keras.layers.Conv2D(filters=512, kernel_size=(3,3), strides=1, padding="same", activation="relu"),
    keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2),

    keras.layers.Conv2D(filters=512, kernel_size=(3,3), strides=1, padding="same", activation="relu"),
    keras.layers.Conv2D(filters=512, kernel_size=(3,3), strides=1, padding="same", activation="relu"),
    keras.layers.Conv2D(filters=512, kernel_size=(3,3), strides=1, padding="same", activation="relu"),
    keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2),

    keras.layers.Flatten(),

    keras.layers.Dense(4096, activation='relu'),
    keras.layers.Dense(4096, activation='relu'),
    keras.layers.Dense(2, activation='softmax')
])

AlexNet.summary()

AlexNet.compile(loss=keras.losses.sparse_categorical_crossentropy,
              optimizer=keras.optimizers.SGD(learning_rate=0.01),
              metrics=[keras.metrics.sparse_categorical_accuracy])

AlexNet_history = AlexNet.fit(X_train, y_train, epochs=10, batch_size=16,
                    validation_data=(X_validation, y_validation))

evaluation = AlexNet.evaluate(X_train, y_train, batch_size=16)
evaluation = AlexNet.evaluate(X_test, y_test, batch_size=16)