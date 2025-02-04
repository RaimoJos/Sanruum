from typing import cast

from langdetect import detect

from sanruum.utils.logger import logger


def detect_language(text: str) -> str:
    """Detect the language of a given text."""
    try:
        language = cast(str, detect(text))  # Explicitly cast
        logger.info(f"Detected language: {language}")
        return language
    except Exception as e:
        logger.error(f"Language detection error: {e}")
        return "unknown"
