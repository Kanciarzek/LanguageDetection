import tensorflow as tf
from .residual_block import ResnetLayer

class SimpleResnet(tf.keras.Model):
    
    def __init__(self, resnets_block_args):
        super(SimpleResnet, self).__init__()
        self.res_module = [ResnetLayer(*res_args) for res_args in resnets_block_args]
        self.gap = tf.keras.layers.GlobalAveragePooling2D()
        self.out = tf.keras.layers.Dense(5, activation=None)
        self.softmax = tf.keras.layers.Softmax()

    def call(self, batch, training=True):
        x = batch
        
        for layer in self.res_module:
            x = layer(x)

        x = self.gap(x)
        x = self.out(x)
        x = self.softmax(x)

        return x

if __name__ == "__main__":

    import numpy as np

    sample_batch = np.ones((25, 200, 300, 1), dtype=np.float32)
    
    res_block_args = [
        [128,3, 1],
        [64, 3, 1],
        [64, 3, 1],
        [32, 3, 1]
    ]

    model = SimpleResnet(res_block_args)
    out = model.predict(sample_batch)
    model.summary()
    print(out)