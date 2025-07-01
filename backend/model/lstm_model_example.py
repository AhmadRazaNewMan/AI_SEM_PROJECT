import keras
def build_lstm_model(input_shape):
    model = keras.Sequential([
        keras.layers.LSTM(128, input_shape=input_shape),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model
    pass  # This is just a placeholder for explanation

# Example of how you would train and save the model

def train_and_save_lstm_model(X_train, y_train, model_path):
    model = build_lstm_model((X_train.shape[1], 1))
    model.fit(X_train, y_train, epochs=5, batch_size=64, validation_split=0.1)
    model.save(model_path)
    pass  # This is just a placeholder for explanation

# Example of how you would load the model

def load_lstm_model(model_path):
    return keras.models.load_model(model_path)
    pass  # This is just a placeholder for explanation 