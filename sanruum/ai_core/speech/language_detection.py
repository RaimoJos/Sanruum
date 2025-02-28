from __future__ import annotations

from langdetect import detect

from sanruum.utils.base.logger import logger


def detect_language(text: str | None) -> str:
    """Detect the language of a given text."""
    if not isinstance(text, str) or not text.strip():
        logger.warning('Invalid input: Text must be a non-empty string.')
        return 'unknown'

    if len(text.split()) < 2:  # Edge case: too short text
        logger.warning('Text is too short for reliable language detection.')
        return 'unknown'

    try:
        # Ensure that detect returns a valid string or handle case where it might not
        language: str | None = detect(text)
        if not isinstance(language, str):
            logger.warning('Language detection returned an unexpected value.')
            return 'unknown'

        logger.info(f'Detected language: {language}')
        return language
    except Exception as e:
        logger.error(f'Language detection error: {e}')
        return 'unknown'
