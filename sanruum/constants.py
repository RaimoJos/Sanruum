# sanruum\constants.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# * # * # * # * # ---------------------------------------------------------------------------------------- # * # * # * #
# -------------------------------------------------- Data directory -------------------------------------------------- #
DATA_DIR = os.path.join(BASE_DIR, "data")  # DATA_DIR
os.makedirs(DATA_DIR, exist_ok=True)
FAQ_FILE = os.path.join(DATA_DIR, "faq.json")  # FAQ_FILE
RESPONSES_FILE = os.path.join(DATA_DIR, "responses.json")  # RESPONSES_FILE
SESSION_HISTORY_FILE = os.path.join(DATA_DIR, "session_history.json")  # SESSION_HISTORY_FILE
USER_MEMORY_DIR = os.path.join(DATA_DIR, "user_memory")  # USER_MEMORY_DIR
os.makedirs(USER_MEMORY_DIR, exist_ok=True)
MEMORY_FILE = os.path.join(DATA_DIR, "ai_memory.json")

# -------------------------------------------------*- Log directory -------------------------------------------------- #
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "sanruum.log")

PROJECT_PATH = os.path.join(BASE_DIR, "sanruum")
NLP_DIR = os.path.join(PROJECT_PATH, "nlp")
os.makedirs(NLP_DIR, exist_ok=True)
MODEL_DIR = os.path.join(NLP_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)
PARAMS_FILE = os.path.join(MODEL_DIR, "best_params.json")
BEST_LOG_REG_FILE = os.path.join(MODEL_DIR, "logistic_regression_model.pkl")
BEST_SVM_FILE = os.path.join(MODEL_DIR, "svm_model.pkl")
RANDOM_FOREST_MODEL_FILE = os.path.join(MODEL_DIR, 'random_forest_model.pkl')
NLP_DATA_DIR = os.path.join(NLP_DIR, "data")
os.makedirs(NLP_DATA_DIR, exist_ok=True)
RAW_TEXT_DATA_DIR = os.path.join(NLP_DATA_DIR, "raw_data")
os.makedirs(RAW_TEXT_DATA_DIR, exist_ok=True)
PROCESSED_DATA_DIR = os.path.join(NLP_DATA_DIR, "processed_data")
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
RAW_DATA_FILE: str = os.path.join(RAW_TEXT_DATA_DIR, "raw_text_data.csv")
PROCESSED_FILE = os.path.join(PROCESSED_DATA_DIR, "processed_text_data.csv")
