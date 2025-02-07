import random
from pathlib import Path

import pandas as pd

from sanruum.constants import RAW_DATA_FILE, PROCESSED_FILE

# Ensure paths are correct
PROCESSED_DATA_FILE = Path(PROCESSED_FILE)
RAW_TEXT_FILE = Path(RAW_DATA_FILE)

# Load raw text data from CSV
try:
    raw_df = pd.read_csv(RAW_TEXT_FILE)
    raw_texts = raw_df["text"].tolist()
    raw_labels = raw_df["label"].tolist()
except Exception as e:
    print(f"Error loading raw text data: {e}")
    raw_texts, raw_labels = [], []

# Manually defined texts
appointment_texts = [
    "I need to book an appointment for next week.",
    "Can I schedule a meeting with the dentist?",
    "When is my next appointment with the doctor?",
    "I'd like to book an appointment for tomorrow.",
    "How do I reschedule my doctor's appointment?",
    "I need to cancel my hair salon appointment.",
    "What time is my scheduled meeting?",
    "Can I change my appointment to another day?",
    "Is there a way to book a same-day appointment?",
]

general_inquiries_texts = [
    "How is the weather today?",
    "What time is it?",
    "Can you tell me a joke?",
    "How are you doing?",
    "Where can I find the nearest grocery store?",
    "What’s the latest news?",
    "How does machine learning work?",
    "Explain artificial intelligence in simple terms.",
    "What’s the capital of France?",
]

# Combine the texts and create corresponding labels
texts = appointment_texts + general_inquiries_texts + raw_texts
labels = ([1] * len(appointment_texts) + [0] * len(general_inquiries_texts) + raw_labels)

# Shuffle the dataset to ensure randomness
data = list(zip(texts, labels))
random.shuffle(data)

# Separate the texts and labels after shuffling
texts, labels = zip(*data)

# Create a DataFrame
df = pd.DataFrame({
    "text": texts,
    "label": labels
})

# Save to CSV
df.to_csv(PROCESSED_DATA_FILE, index=False)

print(f"Dataset created and saved to {PROCESSED_FILE}")
