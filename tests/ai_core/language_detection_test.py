# tests\ai_core\language_detection_test.py
from __future__ import annotations

from typing import Any
from unittest.mock import patch

from sanruum.ai_core.speech.language_detection import detect_language


@patch('sanruum.ai_core.speech.language_detection.detect', return_value='en')
def test_detect_language_success(mock_detect: Any) -> None:
    assert detect_language('This is a test sentence.') == 'en'


def test_detect_language_too_short() -> None:
    assert detect_language('Hi') == 'unknown'


def test_detect_language_invalid_input() -> None:
    assert detect_language('') == 'unknown'  # Empty string case
    assert detect_language(None) == 'unknown'  # None input should return 'unknown'
    # String of numbers should return 'unknown'
    assert detect_language('123') == 'unknown'
    # Non-empty, non-meaningful string should also return 'unknown'
    assert detect_language('123abc') == 'unknown'
