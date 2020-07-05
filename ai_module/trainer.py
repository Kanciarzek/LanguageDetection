import tensorflow as tf

class Trainer:

    def __init__(self, optimizer, epochs = 100, lr = 1e-3):
        self.optim_algos = optimizer
        self.learning_rate = lr
        self.epochs = epochs

        self.METRICS = [ tf.keras.metrics.Accuracy() ]

        #TODO
        #LEARNING RATE SCHEDULAR

    def train(self, data, model, val_data):

        model.compile(
            loss="sparse_categorical_crossentropy",
            optimizer=self.optim_algos,
            metrics=["accuracy"]
            )

        history = model.fit(
            data, epochs=self.epochs, validation_data = val_data)
