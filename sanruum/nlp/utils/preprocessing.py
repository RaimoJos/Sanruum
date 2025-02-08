from __future__ import annotations

import re

import nltk
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# import nltk

# Ensure NLTK data is downloaded
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# Initialize the Lemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


# Preprocess the text
def preprocess_text(text: str) -> str:
    """
    Cleans and processes text by:
    - Expanding constractions (e.g., "I've" -> "I have")
    - Lowercasting
    - Removing special characters
    - Handling negations (e.g., "not happy" -> "not_happy")
    - Removing stopwords
    - Lemmatizing words

    Args:
        text (str): The input text to preprocess.

    Returns:
        str: The cleaned and processed text.
    """
    if not text or not isinstance(text, str):
        return ''

    # Convert text to lowercase
    text = text.lower()

    # Handle negations (e.g., "not happy" → "not_happy")
    text = re.sub(r'not\s(\w+)', r'not_\1', text)

    # Tokenize while keeping only words (removes punctuation)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)

    # Remove stopwords & apply lemmatization
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]

    # Return preprocessed text as a space-separated string
    return ' '.join(tokens)
