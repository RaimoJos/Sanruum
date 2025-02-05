import re

# import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download required NLTK data (run these lines once to download)
# nltk.download('punkt')
# nltk.download('stopwords')

# Initialize the Lemmatizer
lemmatizer = WordNetLemmatizer()


# Preprocess the text
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove non-alphabetic characters (optional based on your needs)
    text = re.sub(r'[^a-z\s]', '', text)

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Return preprocessed text as a space-separated string
    return ' '.join(tokens)
