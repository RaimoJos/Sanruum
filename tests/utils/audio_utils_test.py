from __future__ import annotations

from collections.abc import Generator
from typing import Any
from typing import cast
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from sanruum.utils.audio_utils import listen
from sanruum.utils.audio_utils import speak
from sanruum.utils.logger import logger


# Test for listen function
@pytest.fixture
def mock_listen() -> Generator[MagicMock, Any, None]:
    with patch('speech_recognition.Recognizer.listen') as mock_listen:
        yield mock_listen


@pytest.fixture
def mock_recognize_google() -> Generator[MagicMock, Any, None]:
    with patch(
            'speech_recognition.Recognizer.recognize_google',
    ) as mock_recognize_google:
        yield mock_recognize_google


def test_listen_success(
        mock_listen: MagicMock,
        mock_recognize_google: MagicMock,
) -> None:
    # Mock the recognizer's methods
    mock_listen.return_value = MagicMock()
    mock_recognize_google.return_value = 'Hello'

    result = listen()
    assert result == 'Hello'
    # Explicitly cast the mock to MagicMock before calling assert_called_once
    cast(MagicMock, mock_recognize_google).assert_called_once()


def test_listen_timeout(
        mock_listen: MagicMock,
        mock_recognize_google: MagicMock,
) -> None:
    # Simulate timeout
    mock_listen.side_effect = Exception('Listen timeout')

    result = listen()
    assert result == ''
    cast(MagicMock, logger.warning).assert_called_with('⏳ Listening timed out.')


def test_listen_unknown_value(
        mock_listen: MagicMock,
        mock_recognize_google: MagicMock,
) -> None:
    # Simulate unknown value error
    mock_listen.return_value = MagicMock()
    mock_recognize_google.side_effect = Exception('Unknown value')

    result = listen()
    assert result == ''
    cast(MagicMock, logger.warning).assert_called_with('🛑 Could not understand audio.')


def test_listen_request_error(
        mock_listen: MagicMock,
        mock_recognize_google: MagicMock,
) -> None:
    # Simulate request error
    mock_listen.return_value = MagicMock()
    mock_recognize_google.side_effect = Exception('Request error')

    result = listen()
    assert result == ''
    cast(MagicMock, logger.error).assert_called_with(
        '🔗 Speech recognition service unavailable.',
    )


# Test for speak function
@pytest.fixture
def mock_engine() -> Generator[MagicMock, Any, None]:
    with patch('pyttsx3.init') as mock_init:
        mock_engine_instance = MagicMock()
        mock_init.return_value = mock_engine_instance
        yield mock_engine_instance


def test_speak_success(mock_engine: MagicMock) -> None:
    speak('Test speech')

    cast(MagicMock, mock_engine.say).assert_called_once_with('Test speech')
    cast(MagicMock, mock_engine.runAndWait).assert_called_once()


def test_speak_failure(mock_engine: MagicMock) -> None:
    mock_engine.say.side_effect = Exception('Engine error')

    speak('Test speech failure')

    cast(MagicMock, mock_engine.say).assert_called_once_with('Test speech failure')
    cast(MagicMock, logger.error).assert_called_once_with(
        'Error in text-to-speech: Engine error',
    )
