# sanruum\ai_core\config.py
from __future__ import annotations

import json

from sanruum.constants import RESPONSES_FILE
from sanruum.utils.logger import logger

PERSONALITY_MODE = 'friendly'  # Options: "formal", "friendly", "professional"

# Constants for config
DEFAULT_RESPONSES: dict = {}

try:
    with open(RESPONSES_FILE, encoding='utf-8') as f:
        RESPONSES = json.load(f)
    logger.info('✅ Responses JSON Loaded Successfully!')
except json.JSONDecodeError as e:
    logger.error(f'❌ Failed to Decode Responses JSON: {e}')
    RESPONSES = DEFAULT_RESPONSES
except FileNotFoundError as e:
    logger.warning(f'⚠️ Responses JSON Not Found: {e}')
    RESPONSES = DEFAULT_RESPONSES
except Exception as e:
    logger.error(f'❌ Unexpected Error: {e}')
    RESPONSES = DEFAULT_RESPONSES
