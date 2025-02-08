# sanruum\ai_core\speech\language_detection.py
from __future__ import annotations

from typing import cast

from langdetect import detect

from sanruum.utils.logger import logger


def detect_language(text: str) -> str:
    """Detect the language of a given text."""
    if not text or len(text.split()) < 2:  # Edge case: too short text
        logger.warning('Text is too short for reliable language detection.')
        return 'unknown'
    try:
        language = cast(str, detect(text))  # Explicitly cast
        logger.info(f'Detected language: {language}')
        return language
    except Exception as e:
        logger.error(f'Language detection error: {e}')
        return 'unknown'
