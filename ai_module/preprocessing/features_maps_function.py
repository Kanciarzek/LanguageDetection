import numpy as np
from librosa import power_to_db
from librosa.feature import melspectrogram

def make_melspec_feature(data, sr, n_mels):
    spectogram = melspectrogram(data, sr, n_mels = n_mels)
    spectogram = power_to_db(spectogram, ref=np.max)

    return spectogram.reshape((1, *spectogram.shape))