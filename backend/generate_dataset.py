import numpy as np

# Generate 50,000 sequences, each with 32 notes (MIDI note numbers 60-72)
X = np.random.randint(60, 72, size=(50000, 32))
y = np.random.randint(60, 72, size=(50000, 1))  # Next note prediction

# Save to disk for reuse
np.save('X_notes.npy', X)
np.save('y_notes.npy', y)

# Also save as CSV
np.savetxt('X_notes.csv', X, delimiter=',', fmt='%d')
np.savetxt('y_notes.csv', y, delimiter=',', fmt='%d')

print('Dataset generated and saved as X_notes.npy, y_notes.npy, X_notes.csv, and y_notes.csv') 