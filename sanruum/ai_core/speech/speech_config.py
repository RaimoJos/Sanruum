# sanruum\ai_core\speech\speech_config.py
from __future__ import annotations

from typing import Any

SPEECH_CONFIG = {
    'stt': 'whisper',  # Options: "google", "whisper", "vosk"
    'tts': 'pyttsx3',  # Options: "pyttsx3", "vosk"
    'language': 'en',
    'stt_retry_attempts': 3,  # Retry STT recognition 3 times if it fails
    'tts_retry_attempts': 2,  # Retry TTS synthesis 2 times if it fails
}


def get_speech_config(key: str, default: Any = None) -> Any:
    """Retrieve a speech config value with a default fallback."""
    return SPEECH_CONFIG.get(key, default)
