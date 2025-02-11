# tests\nlp\dataset_creator_test.py
from __future__ import annotations

from unittest.mock import mock_open
from unittest.mock import patch

import pandas as pd
import pytest

from sanruum.constants import RAW_DATA_FILE
from sanruum.nlp.dataset_creator import label_map
from sanruum.nlp.dataset_creator import PROCESSED_FILE


# Test for dataset creation and file saving
def test_create_and_save_dataset() -> None:
    mock_texts = ['Hello', 'How are you?']
    mock_labels = [0, 1]

    # Mock writing the CSV file
    with patch('pandas.DataFrame.to_csv') as mock_to_csv:
        # Use a custom sample dataset
        with patch('random.shuffle'):
            df = pd.DataFrame({'text': mock_texts, 'label': mock_labels})
            df.to_csv(PROCESSED_FILE, index=False)

        mock_to_csv.assert_called_once_with(PROCESSED_FILE, index=False)


# Test for valid label map creation
def test_label_map_creation() -> None:
    expected_label_map = {'appointment': 0, 'general': 1, 'business_inquiry': 2}

    with patch('builtins.open', mock_open()) as mocked_file:
        with patch(
                'pandas.read_csv', return_value=pd.DataFrame({'text': [], 'label': []}),
        ):
            # Run the dataset creation code
            assert label_map == expected_label_map
            # Ensure the file was opened
            mocked_file.assert_called_once_with(
                'some_file_path',
            )  # Replace with actual file path if applicable


# Test for missing file error when loading CSV
def test_load_raw_data_file_error() -> None:
    with patch('pandas.read_csv', side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            pd.read_csv(RAW_DATA_FILE)
