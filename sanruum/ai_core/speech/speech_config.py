# sanruum\ai_core\speech\speech_config.py
from __future__ import annotations

SPEECH_CONFIG = {
    'stt': 'whisper',  # Options: "google", "whisper", "vosk"
    'tts': 'pyttsx3',  # Options: "pyttsx3", "vosk"
    'language': 'en',
    'stt_retry_attempts': 3,  # Retry STT recognition 3 times if it fails
    'tts_retry_attempts': 2,  # Retry TTS synthesis 2 times if it fails
}
