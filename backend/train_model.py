import os
import numpy as np
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import json

MODEL_DIR = 'backend/model'
MODEL_PATH = os.path.join(MODEL_DIR, 'lstm_model.h5')
METRICS_PATH = os.path.join(MODEL_DIR, 'metrics.json')

# --- Data Preprocessing ---
def load_and_preprocess_data():
    if os.path.exists('X_notes.npy') and os.path.exists('y_notes.npy'):
        X = np.load('X_notes.npy')
        y = np.load('y_notes.npy')
        print('Loaded dataset from X_notes.npy and y_notes.npy')
    else:
        # Fallback: generate random note sequences
        X = np.random.randint(60, 72, size=(50000, 32))
        y = np.random.randint(60, 72, size=(50000, 1))
        print('Generated random dataset (fallback)')
    return X, y

def build_lstm_model(input_shape):
    model = keras.Sequential([
        keras.layers.LSTM(128, input_shape=input_shape),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    X, y = load_and_preprocess_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = build_lstm_model((X.shape[1], 1))
    # Reshape for LSTM: (samples, timesteps, features)
    X_train_lstm = X_train.reshape((-1, X.shape[1], 1))
    X_test_lstm = X_test.reshape((-1, X.shape[1], 1))
    model.fit(X_train_lstm, y_train, epochs=5, batch_size=64, validation_split=0.1)
    # Evaluate
    y_pred = model.predict(X_test_lstm)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    # Save model and metrics
    model.save(MODEL_PATH)
    with open(METRICS_PATH, 'w') as f:
        json.dump({'r2': float(r2), 'mse': float(mse), 'rmse': float(rmse)}, f)
    print('Model and metrics saved.')

if __name__ == '__main__':
    main() 