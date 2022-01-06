import tensorflow as tf
import numpy as np
import IPython.display as display

def _bytes_feature(value):
  """Returns a bytes_list from a string / byte."""
  if isinstance(value, type(tf.constant(0))):
    value = value.numpy() # BytesList won't unpack a string from an EagerTensor.
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _float_feature(value):
  """Returns a float_list from a float / double."""
  return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

def _int64_feature(value):
  """Returns an int64_list from a bool / enum / int / uint."""
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def image_example(img, label):
    img_shape = tf.image.decode_png(img).shape

    feature = {
        'height' : _int64_feature(img_shape[0]),
        'width' : _int64_feature(img_shape[1]),
        'depth' : _int64_feature(img_shape[2]),
        'label' : _int64_feature(label),
        'image_raw' : _bytes_feature(img)
    }

    return tf.train.Example(features=tf.train.Features(feature=feature))

image_labels ={
    'Biceps' : 0,
    'Triceps' : 1,
}


with tf.io.TFRecordWriter(record_file) as writer:
    img = open('./train_data/Bi_0.png', 'rb').read()
    label = image_labels['Biceps']
    temp = image_example(img, label)
    writer.write(temp.SerializeToString())


