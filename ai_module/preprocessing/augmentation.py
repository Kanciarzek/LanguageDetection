import tensorflow as tf

def mask_freq(spectogram, no_freq, max_width_masking):
    dims = tf.shape(spectogram)
    n_mels, time = dims[0], dims[1]    
    # max_width_masking = tf.cast(max_width_masking, dtype=tf.int32)

    for i in range(no_freq):
        width = tf.random.uniform([], minval=0, maxval = max_width_masking, dtype=tf.int32)
        position = tf.random.uniform([], minval=0, maxval = n_mels - width, dtype=tf.int32)

        mask = tf.concat(
            [tf.ones(shape=(position, time , 1)),
            tf.zeros(shape=(width, time, 1)),
            tf.ones(shape=(n_mels - position - width, time, 1))], 
            0)

        spectogram = mask * spectogram

    return spectogram

def mask_time(spectogram, no_time, max_width_masking):
    dims = tf.shape(spectogram)
    n_mels, time = dims[0], dims[1]    
    # max_width_masking = tf.cast(max_width_masking, dtype=tf.int32)

    for i in range(no_time):
        width = tf.random.uniform([], minval=0, maxval = max_width_masking, dtype=tf.int32)
        position = tf.random.uniform([], minval=0, maxval = n_mels - width, dtype=tf.int32)

        mask = tf.concat(
            [tf.ones(shape=(n_mels, position, 1)),
            tf.zeros(shape=(n_mels, width, 1)),
            tf.ones(shape=(n_mels, time - position - width, 1))], 
            1)

        spectogram = mask * spectogram

    return spectogram
