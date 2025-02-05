# Some example data
import random

import pandas as pd

from sanruum.constants import RAW_DATA_FILE

appointment_texts = [
    "I need to book an appointment for next week,",
    "Can I schedule a meeting with the dentist?",
    "When is my next appointment with the doctor?",
    "I'd like to book an appointment for tomorrow.",
    "How do I reschedule my doctor's appointment?"
]

general_inquiries_texts = [
    "How is the weather today?",
    "What time is it?",
    "Can you tell me a joke?",
    "How are you doing?",
    "Where can I find the nearest grocery store?"
]

# Combine the texts and create corresponding labels
texts = appointment_texts + general_inquiries_texts
labels = ([1] * len(appointment_texts)
          + [0] * len(general_inquiries_texts))  # 1 = appointment-related, 0 = general inquiry

# Shuffle the dataset to ensure randomness
data = list(zip(texts, labels))
random.shuffle(data)

# Separate the texts and labels
texts, labels = zip(*data)

# Create a DataFrame
df = pd.DataFrame({
    'text': texts,
    'label': labels
})

# Save to CSV for later use
df.to_csv(RAW_DATA_FILE)

print("Dataset created and saved to raw_text_data.csv")
