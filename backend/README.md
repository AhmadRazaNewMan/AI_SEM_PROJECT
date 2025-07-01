# AI Music Composer – Backend Viva Guide

---

## 🚀 Getting Started (from GitHub)

### 1. **Clone the Repository**
If you haven't already, clone the full project from GitHub:
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name/backend
```

### 2. **Install Dependencies**
Make sure you have Python 3.7+ installed. Then run:
```bash
pip install -r requirements.txt
```

### 3. **Generate the Dataset**
```bash
python generate_dataset.py
```

### 4. **Train the Model**
```bash
python train_model.py
```

### 5. **Start the Backend Server**
```bash
python app.py
```
The backend will run at [http://localhost:5000](http://localhost:5000).

---

## 🧑‍💻 Running the Full Project (Frontend + Backend)
See `../frontend/README.md` for instructions on running the frontend and connecting both parts together.

---

## 1. Project Structure

```
backend/
├── app.py                # Flask API
├── generate_dataset.py   # Generates dataset (X_notes.npy/csv, y_notes.npy/csv)
├── train_model.py        # Trains LSTM model
├── requirements.txt      # Python dependencies
├── model/
│   ├── lstm_model.h5     # Saved model (after training)
│   └── metrics.json      # Model evaluation metrics
├── X_notes.npy/csv       # Input dataset (50,000 sequences)
├── y_notes.npy/csv       # Output dataset (next note for each sequence)
```

---

## 2. requirements.txt

```
Flask
flask-cors
numpy
midiutil
```

**What are these and why?**
- **Flask:** For building the backend API (lets frontend talk to backend).
- **flask-cors:** Allows frontend (React) to access backend from a different port (solves CORS issues).
- **numpy:** For generating, saving, and loading datasets (fast math and arrays).
- **midiutil:** For creating MIDI files from note sequences (so you can play/download music).

---

## 3. Dataset Generation (`generate_dataset.py`)

**What does it do?**
- Creates 50,000 random note sequences (each 32 notes long, values 60–71).
- Each sequence is a row in `X_notes.npy`/`X_notes.csv`.
- The next note (target) is in `y_notes.npy`/`y_notes.csv`.
- Saves both `.npy` (fast for Python) and `.csv` (easy to open in Excel).

**Why?**
- This simulates a real music dataset for training/testing the AI model.

---

## 4. Model Training (`train_model.py`)

**What does it do?**
- Loads the dataset from `.npy` files (or generates if missing).
- Splits data into training and testing sets.
- Builds an LSTM model (a type of RNN good for sequences).
- Trains the model to predict the next note in a sequence.
- Evaluates the model using R², MSE, and RMSE.
- Saves the trained model and metrics.

**Line-by-line explanation:**
- `import ...` — Loads required libraries.
- `MODEL_DIR = ...` — Sets where to save the model and metrics.
- `load_and_preprocess_data()` — Loads dataset from file or generates it.
- `build_lstm_model()` — Creates the LSTM neural network.
- `main()` — Runs the training, evaluation, and saving steps.

---

## 5. Flask API (`app.py`)

**Endpoints:**
- `/generate` (POST): Generates a random MIDI file from requested number of notes.
- `/metrics` (GET): Returns the latest model metrics (R², MSE, RMSE).
- `/generate_json` (POST): Returns generated notes and metrics as JSON.
- `/history` (GET): (If present) Returns recent generations.

**How does it work?**
- Receives requests from the frontend.
- Generates music (random or using the model).
- Returns MIDI files and metrics.

---

## 6. Metrics Explained (like you're a child)

- **R² Score (Coefficient of Determination):**
  - Tells you how well the model's predictions match the real answers.
  - 1.0 is perfect, 0.0 means "no better than guessing."
  - Example: If R² = 0.95, the model is very good!

- **MSE (Mean Squared Error):**
  - Measures how far off the predictions are, on average.
  - Lower is better. 0.0 is perfect.
  - Example: If MSE = 0.1, the predictions are very close to the real notes.

- **RMSE (Root Mean Squared Error):**
  - Like MSE, but in the same units as the notes.
  - Lower is better. 0.0 is perfect.
  - Example: If RMSE = 0.3, the predictions are usually less than 1 note away from the real answer.

---

## 7. Backend Flow (Simple)

1. **User clicks Generate on frontend.**
2. **Frontend sends a request to Flask API.**
3. **Backend generates a sequence of notes (using model or random).**
4. **Backend creates a MIDI file and calculates metrics.**
5. **Backend sends MIDI and metrics back to frontend.**
6. **Frontend plays the music and shows the metrics.**

---

## 8. Q&A (Viva Style)

**Q: What is in requirements.txt and why?**  
A: It lists the Python packages needed for the backend: Flask (API), flask-cors (CORS), numpy (math/data), midiutil (MIDI files).

**Q: Why use LSTM?**  
A: LSTM is a type of RNN that remembers long patterns, which is great for music sequences.

**Q: What is the dataset?**  
A: 50,000 rows of random note sequences, each 32 notes long, with the next note as the target.

**Q: What does the model do?**  
A: It learns to predict the next note in a sequence, like guessing what comes next in a song.

**Q: What are R², MSE, RMSE?**  
A: R² shows how good the predictions are (closer to 1 is better). MSE and RMSE show how far off the predictions are (closer to 0 is better).

**Q: What does the API do?**  
A: It lets the frontend ask for new music, get metrics, and download MIDI files.

**Q: What is the flow?**  
A: User → Frontend → Backend → Model → MIDI + Metrics → Frontend → User

---

## 9. Example Viva Questions

- What is Flask?  
  *A Python web framework for building APIs.*

- What is CORS?  
  *A security feature that lets the frontend talk to the backend.*

- What is a MIDI file?  
  *A digital sheet music file that computers can play.*

- Why do you use numpy?  
  *For fast math and handling big arrays of notes.*

- What is the shape of your dataset?  
  *X: (50000, 32), y: (50000, 1)*

---

## 10. Diagram (Flow)

```
[User Input] → [React Frontend] → [Flask API] → [LSTM Model] → [MIDI Output + Metrics] → [Frontend Playback]
```

---

*Prepared for viva/exam. If you have more questions, just ask!* 