import cv2
import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.InteractiveSession(config=config)

image_size = 227

groups_folder_path = '../Data/AAFT_3/'

X_s = []

y = []
# auto_corr       hadamard        midAng
for label in ['Bi', 'Tri']:

    for feature in ['striping_color']:

        for top, dir, f in os.walk(groups_folder_path + label + "/" + feature + "/"):
            # print(f)
            for filename in f:
                # print(groups_folder_path + label + "/" + feature + "/" + filename)
                img = cv2.imread(groups_folder_path + label + "/" + feature + "/" + filename)
                img = cv2.resize(img, None, fx=image_size / img.shape[0], fy=image_size / img.shape[1])

                X_s.append(img / 256)

                if label == 'Bi':
                    y.append(0)
                else:
                    y.append(1)

print(X_s[0].shape)
# print(X_s)
print(len(y))
X = np.array(X_s)
y = np.array(y)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# validation split

X_train, X_validation, y_train, y_validation = train_test_split(X_train, y_train, test_size=0.1, random_state=10,
                                                                stratify=y_train)
print(len(X_train))


model = keras.applications.VGG19(include_top=True, weights=None, input_shape=(227,227,3), pooling=max, classes=2)
model.compile(loss=keras.losses.sparse_categorical_crossentropy, metrics=['accuracy'],
              optimizer=keras.optimizers.SGD(learning_rate=0.01))
model.fit(X_train, y_train, batch_size=16, epochs=10, validation_data=(X_validation, y_validation))