import numpy as np
import tensorflow as tf
from librosa import power_to_db
from librosa.feature import melspectrogram


def factory_melspec_feature(n_mels, sampling_rate):
    def make_melspec_feature(data):
        data = data.numpy()
        data = data.reshape((-1))

        spectogram = melspectrogram(data, sampling_rate, n_mels=n_mels)
        spectogram = power_to_db(spectogram, ref=np.max)
        spectogram = spectogram.reshape((*spectogram.shape, 1))
        spectogram = tf.convert_to_tensor(spectogram, dtype=tf.float32)
        return spectogram

    return make_melspec_feature
