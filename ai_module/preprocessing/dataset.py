import os

import librosa
import numpy as np
from sklearn import preprocessing
from features_maps_function import make_melspec_feature
from tensorflow.keras.utils import Sequence


class VoiceDataset(Sequence):

    def _get_metadata(self):
        data_paths, labels = [], []
        folds = os.listdir(self.data_path)

        self.label_enc = preprocessing.LabelEncoder()
        self.label_enc.fit(folds)
        
        for lang in folds:
            id_label = self.label_enc.transform([lang])
            folder_path = os.path.join(self.data_path, lang)
            
            filenames = os.listdir(folder_path)
            data_paths += [os.path.join(folder_path, fname) for fname in filenames]
            labels += [id_label] * len(filenames)
        
        self.paths_to_audio = data_paths
        self.labels = labels

    def __init__(self, data_path, feature_function, batch_size, feature_args):
        self.data_path = data_path
        self.batch_size = batch_size
        self.feature_function = feature_function
        self.feature_args = feature_args
        self._get_metadata()
        self._indices = np.arange(len(self.labels))

    def on_epoch_end(self):
        np.random.shuffle(self._indices)

    def __len__(self):
        return int(np.ceil(
            len(self.paths_to_audio) / self.batch_size))

    def __getitem__(self, idx):
        batch = []
        labels = []
        batch_idxs = self._indices[idx * self.batch_size : (idx + 1) * self.batch_size]

        for ind in batch_idxs:
            loaded_sample, sr = librosa.core.load(self.paths_to_audio[ind], sr=None)
            batch += [self.feature_function(loaded_sample, sr, *self.feature_args)]
            labels += self.labels[ind]

        return batch, labels

if __name__ == "__main__":
    PATH = "/home/tskrzypczak/Desktop/dataset_voice"
    vd = VoiceDataset(PATH, make_melspec_feature, 64, (128,))
    for i in range(len(vd)):
        print(i)
        vd[i]
        print()