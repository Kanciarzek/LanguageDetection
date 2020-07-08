import tensorflow as tf
from tensorflow.keras.callbacks import LearningRateScheduler, ModelCheckpoint

MODEL_PATH = "/home/tskrzypczak/Desktop/meine_modele"

class Trainer:

    def __init__(self, optimizer, epochs = 100, lr = 1e-3):
        self.optim_algos = optimizer
        self.learning_rate = lr
        self.epochs = epochs

        #TODO
        #LEARNING RATE SCHEDULAR

    def train(self, data, model, val_data, model_name, callbacks):
        mcp_save = ModelCheckpoint(model_name + '.hdf5', save_best_only=True, monitor='val_loss', mode='min')
        callbacks += [mcp_save]

        model.compile(
            loss="sparse_categorical_crossentropy",
            optimizer=self.optim_algos,
            metrics=["accuracy"]
            )
        
        history = model.fit(
            data, epochs=self.epochs, validation_data=val_data, callbacks=callbacks)
