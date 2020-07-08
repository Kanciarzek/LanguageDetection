import os
import time

import neptune
import tensorflow as tf

from models.resnet_model import SimpleResnet, DropoutResnet, DropoutFullConvResnet
from preprocessing.tf_dataset import get_val_dataset, get_dataset
from preprocessing.features_maps_function import factory_melspec_feature
from trainer import Trainer
from neptune_logger import NeptuneLoggerCallback

# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
melspec_feature_mapping = factory_melspec_feature(64, 44100)
voice_dataset = get_dataset(melspec_feature_mapping, 32)
voice_val_dataset = get_val_dataset(melspec_feature_mapping, 32)

res_block_args = [ 
        # [ [128, 3, 1], [64, 3, 1], [32, 3, 1], [16, 3, 1] ],
        # [ [128, 3, 1], [64, 3, 1], [64, 3, 1], [32, 3, 1] ],
        # [ [128, 3, 1], [128, 3, 1], [64, 3, 1], [64, 3, 1], [64, 3, 1], [64, 3, 1], [32, 3, 1], [32, 3, 1] ],
        [ [64, 3, 1], [32, 3, 1], [16, 3, 1] ]
    ]

# model_name = ["smoll networks#1", "medium networks#1", "big_networks#1"]
model_name = ["resnet_drop_fully", "resnet_drop_conv_ful", "resnet_fully"]
architectures = [DropoutResnet, DropoutFullConvResnet, SimpleResnet] 
# epochs = [10, 10, 10]

neptune.init('tomasz-adam-skrzypczak/sandbox')

for j in range(len(res_block_args)):
    for i in range(len(model_name)):

        exp_name = model_name[i] + str(int(time.time())) + '_' + str(j)

        neptune.create_experiment(name=exp_name)
        simple = architectures[i](res_block_args[j])
        optimizer = tf.keras.optimizers.Adam()
        trainer = Trainer(optimizer, 10)
        callbacks = [NeptuneLoggerCallback()]
        trainer.train(voice_dataset, simple, voice_val_dataset, exp_name, callbacks)

        del simple
