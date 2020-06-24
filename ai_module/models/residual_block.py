import tensorflow as tf

class ResnetLayer(tf.keras.Model):

    def __init__(self, filters, kernel_size, strides = 1):
        super(ResnetLayer, self).__init__(name='')

        self.channels_out = filters
        self.conv21 = tf.keras.layers.Conv2D(filters, kernel_size, strides)
        self.nomr1 = tf.keras.layers.BatchNormalization()

        self.conv22 = tf.keras.layers.Conv2D(filters, kernel_size, strides)
        self.nomr2 = tf.keras.layers.BatchNormalization()

        self.short_conv = tf.keras.layers.Conv2D(
            filters, kernel_size=1, strides=strides, padding='same')
        self.batch_short = tf.keras.layers.BatchNormalization()
        self.activ_fun = tf.nn.relu

    def call(self, input_tensor, training=False):
        x = self.conv21(input_tensor)
        x = self.norm1(x, training=training)
        x = self.activ_fun(x)

        x = self.conv22(x)
        x = self.norm2(x)
        
        channels_in = input_tensor.shape[-1]
        if self.channels_out != channels_in or strides != 1:
            res_conn = self.short_conv(input_tensor)
            res_conn = self.batch_short(res_conn)
        else:
            res_conn = input_tensor
            res_conn = self.batch_short(res_conn)
        
        x = tf.keras.layers.add([shortcut, x])
        x = self.activ_fun(x)

        return x
