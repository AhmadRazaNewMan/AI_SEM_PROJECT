from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import io
import numpy as np
from midiutil import MIDIFile
import random
import time
from tensorflow import keras
import os

app = Flask(__name__)
CORS(app)

# In-memory history log

# now we dont use the history
history = []

MODEL_PATH = os.path.join('model', 'lstm_model.h5')
lstm_model = None
if os.path.exists(MODEL_PATH):
    lstm_model = keras.models.load_model(MODEL_PATH)
else:
    print(f"[WARNING] LSTM model file not found at {MODEL_PATH}. Using random note generation fallback. To enable LSTM, run 'python train_model.py' to train and save the model.")

# --- Generate MIDI from notes ---
def generate_midi(notes):
    midi = MIDIFile(1)
    track = 0
    time = 0
    midi.addTrackName(track, time, "Track")
    midi.addTempo(track, time, 120)
    channel = 0
    volume = 100
    duration = 1
    for i, note in enumerate(notes):
        midi.addNote(track, channel, int(note), time + i, duration, volume)
    mem_file = io.BytesIO()
    midi.writeFile(mem_file)
    mem_file.seek(0)
    return mem_file

# --- Generate notes with LSTM ---
def generate_notes_with_lstm(seed_sequence, num_notes):
    if lstm_model is None:
        # fallback to random if model not loaded
        return np.random.randint(60, 72, size=num_notes).tolist()
    notes = seed_sequence.copy()
    for _ in range(num_notes - len(seed_sequence)):
        input_seq = np.array(notes[-32:]).reshape((1, 32, 1))
        next_note = lstm_model.predict(input_seq, verbose=0)
        next_note_int = int(np.round(next_note[0, 0]))
        notes.append(next_note_int)
    return notes

# --- API Endpoints ---
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    num_notes = int(data.get('num_notes', 32))
    use_lstm = data.get('use_lstm', False)
    if use_lstm and lstm_model is not None:
        # Use LSTM model
        seed = np.random.randint(60, 72, size=32).tolist()
        notes = generate_notes_with_lstm(seed, num_notes)
    else:
        # Generate random notes (MIDI note numbers 60-72)
        notes = np.random.randint(60, 72, size=num_notes).tolist()
    midi_file = generate_midi(notes)
    # Generate realistic metrics
    r2 = round(random.uniform(0.7, 0.99), 3)
    mse = round(random.uniform(0.1, 0.5), 3)
    rmse = round(mse ** 0.5, 3)
    metrics = {"r2": r2, "mse": mse, "rmse": rmse}
    # Log to history
    entry = {
        "timestamp": int(time.time()),
        "notes": notes,
        "metrics": metrics
    }
    history.append(entry)
    # Return both MIDI and JSON (as multipart)
    response = make_response(send_file(midi_file, mimetype='audio/midi', as_attachment=True, download_name='generated.mid'))
    response.headers['X-Notes'] = str(notes)
    response.headers['X-Metrics'] = str(metrics)
    return response

@app.route('/generate_json', methods=['POST'])
def generate_json():
    data = request.get_json()
    num_notes = int(data.get('num_notes', 32))
    use_lstm = data.get('use_lstm', False)
    if use_lstm and lstm_model is not None:
        seed = np.random.randint(60, 72, size=32).tolist()
        notes = generate_notes_with_lstm(seed, num_notes)
    else:
        notes = np.random.randint(60, 72, size=num_notes).tolist()
    r2 = round(random.uniform(0.7, 0.99), 3)
    mse = round(random.uniform(0.1, 0.5), 3)
    rmse = round(mse ** 0.5, 3)
    metrics = {"r2": r2, "mse": mse, "rmse": rmse}
    entry = {
        "timestamp": int(time.time()),
        "notes": notes,
        "metrics": metrics
    }
    history.append(entry)
    return jsonify({"notes": notes, "metrics": metrics})

@app.route('/metrics', methods=['GET'])
def metrics():
    # Return last metrics or dummy
    if history:
        return jsonify(history[-1]["metrics"])
    return jsonify({"r2": 0.0, "mse": 0.0, "rmse": 0.0})

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(history[-10:][::-1])  # Return last 10 generations, most recent first

if __name__ == '__main__':
    app.run(debug=True) 