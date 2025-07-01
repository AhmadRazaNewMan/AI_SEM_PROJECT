from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import io
import numpy as np
from midiutil import MIDIFile
import random
import time

app = Flask(__name__)
CORS(app)

# In-memory history log
history = []

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

# --- API Endpoints ---
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    num_notes = int(data.get('num_notes', 32))
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