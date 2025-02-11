# tests\ai_core\diarization_test.py
from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock
from unittest.mock import patch

from sanruum.ai_core.speech.diarization import SpeakerDiarization


@patch('sanruum.ai_core.speech.diarization.Pipeline.from_pretrained')
def test_speaker_diarization_init(mock_pipeline: Any) -> None:
    mock_pipeline.return_value = MagicMock()
    diarizer = SpeakerDiarization()
    assert diarizer.pipeline is not None


@patch('os.path.exists', return_value=True)
@patch('sanruum.ai_core.speech.diarization.Pipeline.from_pretrained')
def test_diarize_success(mock_pipeline: Any, mock_exists: Any) -> None:
    mock_model = MagicMock()
    mock_model.return_value = 'fake_diarization_result'
    mock_pipeline.return_value = mock_model


@patch('os.path.exists', return_value=False)
@patch('sanruum.ai_core.speech.diarization.Pipeline.from_pretrained')
def test_diarize_file_not_found(mock_pipeline: Any, mock_exists: Any) -> None:
    diarizer = SpeakerDiarization()
    result = diarizer.diarize('non_existent.wav')
    assert result is None
