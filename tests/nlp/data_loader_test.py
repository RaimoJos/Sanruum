from __future__ import annotations

from collections.abc import Generator
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch

import pandas as pd
import pytest

from sanruum.nlp.data_loader import load_custom_dataset


# Mock the preprocess_text function for controlled testing
@pytest.fixture
# Correct annotation for a generator
def mock_preprocess_text() -> Generator[MagicMock]:
    with patch('sanruum.nlp.utils.preprocessing.preprocess_text') as mock:
        yield mock


# Test for successful loading of dataset
def test_load_custom_dataset_success(mock_preprocess_text: MagicMock) -> None:
    mock_preprocess_text.return_value = 'processed text'

    # Mock the CSV file content
    mock_csv = 'text,label\nHello,1\nHow are you,0\n'

    with patch('builtins.open', mock_open(read_data=mock_csv)):
        df = load_custom_dataset('mock_path.csv')

    assert isinstance(df, pd.DataFrame)
    assert 'processed_text' in df.columns
    assert df['processed_text'].iloc[0] == 'processed text'
    assert df['label_name'].iloc[0] == 'General Inquiry'


# Test for missing 'text' column in CSV
def test_load_custom_dataset_missing_text(mock_preprocess_text: MagicMock) -> None:
    mock_csv = 'label\n1\n0\n'

    with patch('builtins.open', mock_open(read_data=mock_csv)):
        with pytest.raises(ValueError):
            load_custom_dataset('mock_path.csv')


# Test for file not found error
def test_load_custom_dataset_file_not_found() -> None:
    with patch('pathlib.Path.exists', return_value=False):
        with pytest.raises(FileNotFoundError):
            load_custom_dataset('mock_path.csv')
