import tensorflow as tf
from residual_block import ResnetLayer

class SimpleResnet(tf.keras.Model):
    
    def __init__(self, resnets_block_args):
        super(SimpleResnet, self).__init__()

        self.res_module = [ResnetLayer(*resnets_block_args) for res_args in resnets_block_args]
        self.gap = tf.keras.layers.GlobalAveragePooling2D()
        self.out = tf.keras.layers.Dense(5, activation=None)

    def call(self, batch, training=True):
        x = self.res_module(batch)
        x = self.gap(x)
        x self.out(x)

        return x
