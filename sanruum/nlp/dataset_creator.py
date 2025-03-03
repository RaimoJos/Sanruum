# sanruum\nlp\dataset_creator.py
from __future__ import annotations

import json
import random
from pathlib import Path

import pandas as pd

from sanruum.config import BaseConfig

LABEL_MAP_FILE = BaseConfig.DATA_DIR / 'label_map.json'
PROCESSED_FILE = BaseConfig.PROCESSED_DATA_DIR / 'processed_text_data.csv'
RAW_DATA_FILE = BaseConfig.RAW_TEXT_DATA_DIR / 'raw_text_data.csv'

# Ensure paths are correct
PROCESSED_DATA_FILE = Path(PROCESSED_FILE)
RAW_TEXT_FILE = Path(RAW_DATA_FILE)

# Load raw text data from CSV
try:
    raw_df = pd.read_csv(RAW_TEXT_FILE)
    raw_texts = raw_df['text'].tolist()
    raw_labels = raw_df['label'].tolist()
except Exception as e:
    print(f'Error loading raw text data: {e}')
    raw_texts, raw_labels = [], []

# Manually defined texts
intent_classes = {
    'appointment': [
        'I need to book an appointment for next week.',
        'Can I schedule a meeting with the dentist?',
        'I want to change my appointment time.',
        'How do I cancel my booking?',
        'Is there a way to book a same-day appointment?',
    ],
    'general': [
        'How is the weather today?',
        'What time is it?',
        'Can you tell me a joke?',
        'How are you doing?',
        'What’s the capital of France?',
    ],
    'business_inquiry': [
        'Do you offer enterprise solutions?',
        'How can I contact your sales team?',
        'What are your pricing plans?',
        'Can I book a demo of your services?',
        'Do you offer AI integration services?',
    ],
}

# Assign numeric labels
label_map = {label: idx for idx, label in enumerate(intent_classes.keys())}

# Combine the texts and labels
texts = []
labels = []

for intent, phrases in intent_classes.items():
    texts.extend(phrases)
    labels.extend([label_map[intent]] * len(phrases))

# Add raw data if available
texts += raw_texts
labels += raw_labels

# Shuffle the dataset for randomness
data = list(zip(texts, labels))
random.shuffle(data)

# Separate the texts and labels after shuffling
texts, labels = (list(t) for t in zip(*data))

# Save dataset
df = pd.DataFrame({'text': texts, 'label': labels})
df.to_csv(PROCESSED_DATA_FILE, index=False)

# Save label map for later use
with open(LABEL_MAP_FILE, 'w') as f:
    json.dump(label_map, f)

print(f'Dataset created and saved to {PROCESSED_FILE}')
