from pathlib import Path

import pandas as pd

from sanruum.constants import RAW_DATA_FILE
from sanruum.utils.logger import logger
from utils.preprocessing import preprocess_text


# Function to load and preprocess the dataset
def load_custom_dataset(file_path):
    """
    Loads the custom dataset from a CSV file and returns the data as a pandas DataFrame.

    Args:
        file_path (str or Path): Path to the CSV file containing the dataset.

    Returns:
        pandas.DataFrame: The dataset loaded as a DataFrame.
    """
    file_path = Path(file_path)  # Ensure it's a Path object

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {file_path}")

    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except Exception as e:
        raise ValueError(f"Error loading CSV file: {e}")

    if "text" not in df.columns:
        raise ValueError("Missing required column: 'text' in dataset.")

    try:
        df["processed_text"] = df["text"].apply(preprocess_text)
    except Exception as e:
        logger.warning(f"Preprocessing failed: {e}")
        df["processed_text"] = df["text"]  # Fallback to raw text

    return df


# Usage example
if __name__ == "__main__":
    df = load_custom_dataset(RAW_DATA_FILE)
    print(df.head())
