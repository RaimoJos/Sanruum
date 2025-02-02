import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# Data directory
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
FAQ_FILE = os.path.join(DATA_DIR, "faq.json")
RESPONSES_FILE = os.path.join(DATA_DIR, "responses.json")

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "sanruum.log")

PROJECT_PATH = os.path.join(BASE_DIR, "sanruum")
