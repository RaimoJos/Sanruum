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

# -------------------------------------------------*- Log directory -------------------------------------------------- #
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "sanruum.log")

PROJECT_PATH = os.path.join(BASE_DIR, "sanruum")
