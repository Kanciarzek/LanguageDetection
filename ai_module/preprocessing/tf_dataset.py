import os

import numpy as np
import librosa
import tensorflow as tf
import tensorflow_io as tfio

from .augmentation import mask_freq, mask_time
from sklearn import preprocessing


PATH = "/home/tskrzypczak/Desktop/dataset_voice/[!validation]*/*"
VAL_PATH = "/home/tskrzypczak/Desktop/dataset_voice/validation/*"
AUTOTUNE = tf.data.experimental.AUTOTUNE

label_enc = preprocessing.LabelEncoder()
label_enc.fit(["chinese", "english", "german", "polish", "russian"])

def get_label(path_file):
    print(path_file)
    label = tf.strings.split(path_file, '/')[-2]    
    label = label.numpy().decode('ascii')
    label = label_enc.transform([label])
    return tf.convert_to_tensor(label, dtype=tf.int32)

def get_val_label(path_file):
    print(path_file)
    
    label = tf.strings.split(path_file, '/')[-1]
    label = tf.strings.split(label, "_")[0]
    
    label = label.numpy().decode('ascii')
    label = label_enc.transform([label])
    return tf.convert_to_tensor(label, dtype=tf.int32)


def load_sample(filepath):

    audio = tf.io.read_file(filepath)
    audio, sr = tf.audio.decode_wav(audio, desired_channels=1)
    return tf.convert_to_tensor(audio, dtype=tf.float32)


def create_dataset(feature_mapping, batch_size, train = True, path_dataset = PATH):
    label_func = get_label if train else get_val_label  

    dt = tf.data.Dataset.list_files(path_dataset).cache()
    dt = dt.shuffle(30000, reshuffle_each_iteration=True)
    dt = dt.map(lambda p : 
            ((load_sample(p), tf.py_function(label_func, inp=[p], Tout=tf.int32))))
    dt = dt.map(lambda sample, label : (
        tf.py_function(feature_mapping, inp=[sample], Tout=[tf.float32]), label))
    dt = dt.map(lambda sample, label: (tf.squeeze(sample, axis=0), tf.squeeze(label, axis=0)))

    if train:
        dt = dt.map(lambda sample, label: (mask_freq(sample, 2, 10), label))
        dt = dt.map(lambda sample, label: (mask_time(sample, 3, 20), label))

    dt = dt.padded_batch(batch_size, padded_shapes=([None, None, 1], []))
    
    return dt


def get_val_dataset(feature_mapping, batch_size):
    return create_dataset(feature_mapping, batch_size, False, VAL_PATH)

def get_dataset(feature_mapping, batch_size):
    return create_dataset(feature_mapping, batch_size, True, PATH)
