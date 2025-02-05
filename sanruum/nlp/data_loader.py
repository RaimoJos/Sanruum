import pandas as pd

from utils.preprocessing import preprocess_text


# Function to load and preprocess the dataset
def load_custom_dataset(file_path):
    """
    Loads the custom dataset from a CSV file and returns the data as a pandas DataFrame.

    Args:
        file_path (str): Path to the CSV file containing the dataset.

    Returns:
        pandas.DataFrame: The dataset loaded as a DataFrame.
    """
    # Load the dataset from CSV
    df = pd.read_csv(file_path)

    # Apply preprocessing to the text column
    df['processed_text'] = df['text'].apply(preprocess_text)

    return df


# Usage example
if __name__ == "__main__":
    df = load_custom_dataset('sanruum/nlp/data/raw_data/raw_text_data.csv')
    print(df.head())
