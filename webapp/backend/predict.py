import audioread
import numpy as np
from librosa import power_to_db, load, display
from librosa.feature import melspectrogram

from webapp.backend.config import SAMPLING_RATE, NUMBER_OF_MELS


def make_melspec_feature(data):
    data = data.reshape((-1))

    spectogram = melspectrogram(data, SAMPLING_RATE, n_mels=NUMBER_OF_MELS)
    spectogram = power_to_db(spectogram, ref=np.max)
    spectogram = spectogram.reshape((*spectogram.shape, 1))
    return spectogram


def preprocess(file):
    audio, sr = load('audio.wav')

    spectrogram = make_melspec_feature(audio)
    print(spectrogram)
    spectrogram = spectrogram.reshape((NUMBER_OF_MELS, -1))
    spectrogram = (spectrogram - np.min(spectrogram)) / (np.max(spectrogram) - np.min(spectrogram))
    return spectrogram
