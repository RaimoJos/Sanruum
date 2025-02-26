# sanruum\constants.py
from __future__ import annotations

import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


# Data directory
def ensure_dir(path: str) -> None:
    """Ensure that the given directory exists."""
    os.makedirs(path, exist_ok=True)


README_FILE = os.path.join(BASE_DIR, 'README.md')
TEST_DIR = os.path.join(BASE_DIR, 'tests')
ensure_dir(TEST_DIR)
DATA_DIR = os.path.join(BASE_DIR, 'data')  # DATA_DIR
ensure_dir(DATA_DIR)
INTENTS_FILE = os.path.join(DATA_DIR, 'intents.json')
OUTPUT_MP3_FILE = os.path.join(DATA_DIR, 'output.mp3')  # OUTPUT_MP3
SESSION_HISTORY_FILE = os.path.join(
    DATA_DIR,
    'session_history.json',
)  # SESSION_HISTORY_FILE
USER_MEMORY_DIR = os.path.join(DATA_DIR, 'user_memory')  # USER_MEMORY_DIR
ensure_dir(USER_MEMORY_DIR)
MEMORY_FILE = os.path.join(DATA_DIR, 'ai_memory.json')
LABEL_MAP_FILE = os.path.join(DATA_DIR, 'label_map.json')
CUSTOM_SUB_CSV_FILE_PATH = os.path.join(DATA_DIR, 'custom_substitutions.csv')
IGNORE_SPELLCHECK_WORD_FILE_PATH = os.path.join(DATA_DIR, 'ignore_spellcheck_words.txt')
DEFAULT_DB_URL = f"sqlite:///{os.path.join(DATA_DIR, 'sanruum.db')}"
DATABASE_URL = os.getenv('DATABASE_URL', DEFAULT_DB_URL)  # Log directory
LOG_DIR = os.path.join(BASE_DIR, 'logs')
ensure_dir(LOG_DIR)
LOG_FILE = os.path.join(LOG_DIR, 'sanruum.log')

PROJECT_PATH = os.path.join(BASE_DIR, 'sanruum')
NLP_DIR = os.path.join(PROJECT_PATH, 'nlp')
ensure_dir(NLP_DIR)
MODEL_DIR = os.path.join(NLP_DIR, 'models')
ensure_dir(MODEL_DIR)
PARAMS_FILE = os.path.join(MODEL_DIR, 'best_params.json')
BEST_LOG_REG_FILE = os.path.join(MODEL_DIR, 'logistic_regression_model.pkl')
BEST_SVM_FILE = os.path.join(MODEL_DIR, 'svm_model.pkl')
RANDOM_FOREST_MODEL_FILE = os.path.join(MODEL_DIR, 'random_forest_model.pkl')
NLP_DATA_DIR = os.path.join(NLP_DIR, 'data')
ensure_dir(NLP_DATA_DIR)
RAW_TEXT_DATA_DIR = os.path.join(NLP_DATA_DIR, 'raw_data')
ensure_dir(RAW_TEXT_DATA_DIR)
PROCESSED_DATA_DIR = os.path.join(NLP_DATA_DIR, 'processed_data')
ensure_dir(PROCESSED_DATA_DIR)
RAW_DATA_FILE: str = os.path.join(RAW_TEXT_DATA_DIR, 'raw_text_data.csv')
PROCESSED_FILE = os.path.join(PROCESSED_DATA_DIR, 'processed_text_data.csv')
