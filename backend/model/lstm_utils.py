import os
from tensorflow import keras

def build_lstm_model(input_shape):
    model = keras.Sequential([
        keras.layers.LSTM(128, input_shape=input_shape),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def load_lstm_model(model_path):
    if os.path.exists(model_path):
        return keras.models.load_model(model_path)
    return None 