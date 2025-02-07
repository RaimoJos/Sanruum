import re

import nltk
# import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Ensure NLTK data is downloaded
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download('wordnet', quiet=True)

# Initialize the Lemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


# Preprocess the text
def preprocess_text(text):
    """
    Cleans and processes text by lowercasing, removing non-alphabetic characters,
    tokenizing, removing stopwords, and applying lemmatization.

    Args:
        text (str): The input text to preprocess.

    Returns:
        str: The cleaned and processed text.
    """
    if not text or not isinstance(text, str):
        return ""

    # Convert text to lowercase
    text = text.lower()

    # Remove non-alphabetic characters (optional based on your needs)
    text = re.sub(r'[^a-z\s]', '', text)

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords and apply lemmatization
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]

    # Return preprocessed text as a space-separated string
    return ' '.join(tokens)
