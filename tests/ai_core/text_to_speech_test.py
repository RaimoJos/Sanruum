# tests\ai_core\text_to_speech_test.py
from __future__ import annotations

from unittest import mock
from unittest.mock import MagicMock

import pytest
from pydub import AudioSegment

from sanruum.ai_core.speech.text_to_speech import play_audio


# Test the 'pygame' playback method
@mock.patch('pygame.mixer.music.play')
@mock.patch('pygame.mixer.music.load')
@mock.patch('pygame.mixer.init')
def test_play_audio_pygame(
        mock_init: MagicMock, mock_load: MagicMock, mock_play: MagicMock,
) -> None:
    mock_play.return_value = None
    filename = 'test.mp3'
    play_audio(filename, method='pygame')
    mock_init.assert_called_once()
    mock_load.assert_called_once_with(filename)
    mock_play.assert_called_once()


# Test the 'pydub' playback method
@mock.patch('pydub.playback.play')
@mock.patch('pydub.AudioSegment.from_file')
def test_play_audio_pydub(mock_from_file: MagicMock, mock_play: MagicMock) -> None:
    mock_play.return_value = None
    mock_from_file.return_value = AudioSegment.silent(duration=1000)
    filename = 'test.mp3'
    play_audio(filename, method='pydub')
    mock_from_file.assert_called_once_with(filename, format='mp3')
    mock_play.assert_called_once()


# Test an unsupported playback method
def test_play_audio_invalid_method() -> None:
    filename = 'test.mp3'
    with pytest.raises(ValueError, match='Unsupported playback method'):
        play_audio(filename, method='invalid')


# Test the default 'pygame' method without specifying the method
@mock.patch('pygame.mixer.music.play')
@mock.patch('pygame.mixer.music.load')
@mock.patch('pygame.mixer.init')
def test_play_audio_default(
        mock_init: MagicMock, mock_load: MagicMock, mock_play: MagicMock,
) -> None:
    filename = 'test.mp3'
    play_audio(filename)
    mock_init.assert_called_once()
    mock_load.assert_called_once_with(filename)
    mock_play.assert_called_once()
