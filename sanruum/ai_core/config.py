import json

from sanruum.constants import RESPONSES_FILE
from sanruum.utils.logger import logger

PERSONALITY_MODE = "friendly"  # Options: "formal", "friendly", "professional"

try:
    with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
        RESPONSES = json.load(f)
    logger.info("✅ Responses JSON Loaded Successfully!")
except Exception as e:
    logger.error(f"❌ Failed to Load Responses JSON: {e}")
    RESPONSES = {}
