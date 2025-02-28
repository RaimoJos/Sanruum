from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
import speech_recognition as sr

from sanruum.utils.base.audio_utils import listen


@pytest.fixture
def dummy_microphone() -> MagicMock:
    """Provides a mocked microphone fixture for tests."""
    return MagicMock()


@pytest.fixture
def mock_recognizer() -> MagicMock:
    recognizer = MagicMock()
    recognizer.listen = MagicMock()  # ✅ Define `.listen` in the fixture
    return recognizer


@pytest.fixture
def mock_recognizer_listen() -> MagicMock:
    return MagicMock()


def test_listen_success(
        dummy_microphone: MagicMock,
        mock_recognizer: MagicMock,
        mock_recognizer_listen: MagicMock,
) -> None:
    """Test successful audio recognition."""
    mock_recognizer_listen.return_value = MagicMock()
    mock_recognizer.recognize_google.return_value = 'Test'
    # Ensure the listen method uses our mock:
    mock_recognizer.listen = mock_recognizer_listen

    with patch(
            'sanruum.utils.base.audio_utils.sr.Recognizer',
            return_value=mock_recognizer,
    ), patch(
        'sanruum.utils.base.audio_utils.sr.Microphone',
        return_value=dummy_microphone,
    ):
        result = listen()
        assert result == 'Test'


def test_listen_timeout(
        dummy_microphone: MagicMock,
        mock_recognizer: MagicMock,
        mock_recognizer_listen: MagicMock,
) -> None:
    """Test handling of timeout error during listening."""
    mock_recognizer_listen.side_effect = sr.WaitTimeoutError
    # Assign the custom listen fixture to the recognizer's listen method:
    mock_recognizer.listen = mock_recognizer_listen

    with patch(
            'sanruum.utils.base.audio_utils.sr.Recognizer',
            return_value=mock_recognizer,
    ), patch(
        'sanruum.utils.base.audio_utils.sr.Microphone',
        return_value=dummy_microphone,
    ):
        result = listen()
        assert result == ''


def test_listen_unknown_value(
        dummy_microphone: MagicMock,
        mock_recognizer: MagicMock,
) -> None:
    mock_recognizer.recognize_google.side_effect = sr.UnknownValueError

    with patch(
            'sanruum.utils.base.audio_utils.sr.Recognizer',
            return_value=mock_recognizer,
    ), patch(
        'sanruum.utils.base.audio_utils.sr.Microphone',
        return_value=dummy_microphone,
    ):
        result = listen()
        assert result == ''


def test_listen_request_error(
        dummy_microphone: MagicMock,
        mock_recognizer: MagicMock,
) -> None:
    mock_recognizer.recognize_google.side_effect = sr.RequestError(
        'Test error',
    )  # Define inside test

    with patch(
            'sanruum.utils.base.audio_utils.sr.Recognizer',
            return_value=mock_recognizer,
    ), patch(
        'sanruum.utils.base.audio_utils.sr.Microphone',
        return_value=dummy_microphone,
    ):
        result = listen()
        assert result == ''
