from __future__ import annotations

import json

from sanruum.config import BaseConfig  # Import BaseConfig
from sanruum.utils.base.logger import logger

DEFAULT_INTENTS: dict = {}

# Access INTENTS_FILE through BaseConfig
INTENTS_FILE = BaseConfig.INTENTS_DIR / 'intents.json'

try:
    with open(INTENTS_FILE, encoding='utf-8') as f:
        INTENTS = json.load(f)
    logger.info('✅ Responses JSON Loaded Successfully!')
except json.JSONDecodeError as e:
    logger.error(f'❌ Failed to Decode Responses JSON: {e}')
    INTENTS = DEFAULT_INTENTS
except FileNotFoundError as e:
    logger.warning(f'⚠️ Responses JSON Not Found: {e}')
    INTENTS = DEFAULT_INTENTS
except Exception as e:
    logger.error(f'❌ Unexpected Error: {e}')
    INTENTS = DEFAULT_INTENTS
