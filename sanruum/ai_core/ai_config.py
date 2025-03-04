from __future__ import annotations

import json
import logging

from sanruum.config import BaseConfig

logger = logging.getLogger(__name__)

DEFAULT_INTENTS: dict = {}

# Access INTENTS_FILE through BaseConfig
INTENTS_FILE = BaseConfig.INTENTS_FILE

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
