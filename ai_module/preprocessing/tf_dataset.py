import os

import numpy as np
import librosa
import tensorflow as tf

from sklearn import preprocessing


PATH = "/home/tskrzypczak/Desktop/dataset_voice/[!validation]*/*"
VAL_PATH = "/home/tskrzypczak/Desktop/dataset_voice/validation/*"
AUTOTUNE = tf.data.experimental.AUTOTUNE

label_enc = preprocessing.LabelEncoder()
label_enc.fit(["chinese", "engilsh", "german", "polish", "russian"])

def get_label(path_file):
    label = tf.strings.split(path_file, '/')[-2]
    label = label.numpy().decode('ascii')
    label = label_enc.transform([label])

    return tf.convert_to_tensor(label, dtype=tf.int32)


def load_sample(filepath):
    audio = tf.io.read_file(filepath)
    audio, sr = tf.audio.decode_wav(audio, desired_channels=1)
    return tf.convert_to_tensor(audio, dtype=tf.float32)


def create_dataset(feature_mapping, batch_size, path_dataset = PATH):
    dt = tf.data.Dataset.list_files(PATH).cache()
    dt = dt.shuffle(30000, reshuffle_each_iteration=True)
    dt = dt.map(lambda p : 
            (load_sample(p), tf.py_function(get_label, inp=[p], Tout=tf.int32)), 
        num_parallel_calls=AUTOTUNE)
    dt = dt.map(lambda sample, label : (
        tf.py_function(feature_mapping, inp=[sample], Tout=[tf.float32]), label),
        num_parallel_calls=AUTOTUNE)
    dt = dt.map(lambda sample, label: 
            (tf.squeeze(sample, axis=0), tf.squeeze(label, axis=0)))
    dt = dt.padded_batch(batch_size, 
            padded_shapes=([None, None, 1], [])).prefetch(AUTOTUNE)
    
    return dt

def get_val_dataset(feature_mapping, batch_size):
    return create_dataset(feature_mapping, batch_size, VAL_PATH)

def get_dataset(feature_mapping, batch_size):
    return create_dataset(feature_mapping, batch_size, PATH)
