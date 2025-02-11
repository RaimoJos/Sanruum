# tests\nlp\preprocessing_test.py
# tests/preprocessing_test.py
from __future__ import annotations

from sanruum.nlp.utils.preprocessing import preprocess_text


def test_preprocess_text() -> None:
    # Test with simple sentence
    text = 'I am running late!'
    result = preprocess_text(text)
    assert result == 'run late', f"Expected 'run late', but got {result}"

    # Test with stopwords
    text = 'This is a test.'
    result = preprocess_text(text)
    assert result == 'test', f"Expected 'test', but got {result}"

    # Test negation handling
    text = 'I am not happy'
    result = preprocess_text(text)
    assert result == 'not_happy', f"Expected 'not_happy', but got {result}"

    # Test with punctuation and lowercasing
    text = "I can't do this."
    result = preprocess_text(text)
    assert result == 'can not do', f"Expected 'can not do', but got {result}"

    # Test empty text
    text = ''
    result = preprocess_text(text)
    assert result == '', 'Expected an empty string, but got a result'
