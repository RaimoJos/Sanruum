from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

from speech_recognition import WaitTimeoutError

from sanruum.ai_core.speech.speech_recognition import SpeechRecognition


def test_recognize_speech_google() -> None:
    recognizer = SpeechRecognition(engine='google')

    # Mock the '_recognize_google' method using patch.object
    with patch.object(recognizer, '_recognize_google', return_value='Hello world'):
        with patch.object(recognizer.recognizer, 'listen', return_value=MagicMock()):
            result = recognizer.recognize_speech()
            assert result == 'Hello world'


def test_recognize_speech_whisper() -> None:
    recognizer = SpeechRecognition(engine='whisper')

    # Mock the '_recognize_whisper' method using patch.object
    with patch.object(recognizer, '_recognize_whisper', return_value='Whisper test'):
        with patch.object(recognizer.recognizer, 'listen', return_value=MagicMock()):
            result = recognizer.recognize_speech()
            assert result == 'Whisper test'


def test_recognize_speech_timeout() -> None:
    recognizer = SpeechRecognition(engine='google')

    # Mock the 'listen' method to raise WaitTimeoutError
    with patch.object(recognizer.recognizer, 'listen', side_effect=WaitTimeoutError):
        result = recognizer.recognize_speech()
        assert result == ''
