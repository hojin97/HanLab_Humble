import tensorflow as tf
from tensorflow import keras

import numpy as np

config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.4
session = tf.compat.v1.InteractiveSession(config=config)

import os, re, glob
import cv2

image_size = 227

#groups_folder_path = '../Images/After_AAFT/'
#groups_folder_path = '../Images/After_image/'
groups_folder_path = '../Images/After_resultFigs/'

X_s = []

y = []

for label in ['Bi', 'Tri']:

    for feature in ['striping_bw']:

        for top, dir, f in os.walk(groups_folder_path + label + "/" + feature + "/"):
            print(f)
            for filename in f:
                # print(groups_folder_path + label + "/" + feature + "/" + filename)
                img = cv2.imread(groups_folder_path + label + "/" + feature + "/" + filename)
                img = cv2.resize(img, None, fx=image_size / img.shape[0], fy=image_size / img.shape[1])

                X_s.append(img / 256)

                if label == 'Bi':
                    y.append(2)
                else:
                    y.append(3)

print(X_s[0])

X = np.array(X_s)
y = np.array(y)
