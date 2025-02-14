# tests/ai_core/speech_recognition_test.py
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

from speech_recognition import WaitTimeoutError

from sanruum.ai_core.speech.speech_recognition import SpeechRecognition


def test_recognize_speech_google() -> None:
    dummy_microphone = MagicMock()
    dummy_microphone.__enter__.return_value = MagicMock()
    dummy_microphone.__exit__.return_value = None
    speech_recog = SpeechRecognition(engine='google', microphone=dummy_microphone)

    # Mock the '_recognize_google' method using patch.object
    with patch.object(speech_recog, '_recognize_google', return_value='Hello world'):
        with patch.object(speech_recog.recognizer, 'listen', return_value=MagicMock()):
            result = speech_recog.recognize_speech()
            assert result == 'Hello world'


def test_recognize_speech_whisper() -> None:
    dummy_microphone = MagicMock()
    dummy_microphone.__enter__.return_value = MagicMock()
    dummy_microphone.__exit__.return_value = None
    speech_recog = SpeechRecognition(engine='whisper', microphone=dummy_microphone)

    # Mock the '_recognize_whisper' method using patch.object
    with patch.object(speech_recog, '_recognize_whisper', return_value='Whisper test'):
        with patch.object(speech_recog.recognizer, 'listen', return_value=MagicMock()):
            result = speech_recog.recognize_speech()
            assert result == 'Whisper test'


def test_recognize_speech_timeout() -> None:
    dummy_microphone = MagicMock()
    dummy_microphone.__enter__.return_value = MagicMock()
    dummy_microphone.__exit__.return_value = None
    speech_recog = SpeechRecognition(engine='google', microphone=dummy_microphone)

    # Mock the 'listen' method to raise WaitTimeoutError
    with patch.object(speech_recog.recognizer, 'listen', side_effect=WaitTimeoutError):
        result = speech_recog.recognize_speech()
        assert result == ''
