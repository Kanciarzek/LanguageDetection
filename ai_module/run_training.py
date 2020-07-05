import tensorflow as tf
import os

from models.resnet_model import SimpleResnet
from preprocessing.tf_dataset import get_val_dataset, get_dataset
from preprocessing.features_maps_function import factory_melspec_feature
from trainer import Trainer


# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
melspec_feature_mapping = factory_melspec_feature(64, 44100)
voice_dataset = get_dataset(melspec_feature_mapping, 32)
voice_val_dataset = get_val_dataset(melspec_feature_mapping, 32)

res_block_args = [
    [128, 3, 1],
    [64, 3, 1],
    [32, 3, 1],
    [32, 3, 1],
]

simple = SimpleResnet(res_block_args)
optimizer = tf.keras.optimizers.Adam()
trainer = Trainer(optimizer)
trainer.train(voice_dataset, simple, voice_val_dataset)
