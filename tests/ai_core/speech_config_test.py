# tests\ai_core\speech_config_test.py
from __future__ import annotations

from sanruum.ai_core.speech.speech_config import get_speech_config


def test_get_speech_config() -> None:
    assert get_speech_config('stt') == 'whisper'
    assert get_speech_config('language') == 'en'
    assert get_speech_config('non_existent', 'default_value') == 'default_value'
