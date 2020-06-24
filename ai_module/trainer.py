import tensorflow as tf

class Trainer:

    def __init__(self, optimizer, epochs = 100, lr = 1e-3):
        self.optim_algos = optimizer
        self.learning_rate = lr
        self.epochs = epochs

        self.METRICS = [ tf.keras.metrics.Accurany() ]

        #TODO
        #LEARNING RATE SCHEDULAR

    def train(self, data_sequence, model):

        model.compile(
            loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False),
            optimizer=self.optim_algos,
            metrics=self.METRICS
            )

        history = model.fit(data_sequence, epochs=self.epochs)
        

