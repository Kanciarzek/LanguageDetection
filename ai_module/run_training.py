import tensorflow as tf

from models.resnet_model import SimpleResnet
from preprocessing.dataset import VoiceDataset
from preprocessing.features_maps_function import make_melspec_feature
from trainer import Trainer


PATH = "/home/tskrzypczak/Desktop/dataset_voice"
voice_dataset = VoiceDataset(PATH, make_melspec_feature, 32, (128,))

res_block_args = [
    [128, 3, 1],
    [128, 3, 1],
    [64, 3, 1],
    [64, 3, 1],
    [32, 3, 1],
    [32, 3, 1],
]

simple = SimpleResnet(res_block_args)
optimizer = tf.keras.optimizers.Adam()
trainer = Trainer(optimizer)

print(len(voice_dataset[0][1]))

print(voice_dataset[0][0].shape)#, voice_dataset[0][1].shape)
trainer.train(voice_dataset, simple)

