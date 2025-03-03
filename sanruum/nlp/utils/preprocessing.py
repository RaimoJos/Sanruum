from __future__ import annotations

import re
from collections.abc import Callable
from functools import wraps
from pathlib import Path
from typing import Any
from unicodedata import normalize

import contractions
import nltk
from names_dataset import NameDataset
from nltk import LancasterStemmer
from nltk import PunktSentenceTokenizer
from nltk import SnowballStemmer
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem.snowball import PorterStemmer
from nltk.tokenize import word_tokenize
from spellchecker.spellchecker import SpellChecker

from sanruum.config import BaseConfig
from sanruum.utils.base.logger import logger

IGNORE_SPELLCHECK_WORD_FILE_PATH = (
    BaseConfig.directories.DATA_DIR
    / 'ignore_spellcheck_words.txt'
)

nltk.download('stopwords')

# Global precompiled regex patterns for performance
URL_REGEX = re.compile(r'(www|http)\S+')
ITEMIZED_REGEX = re.compile(r'[(\s][0-9a-zA-Z][.)]\s+|[(\s][ivxIVX]+[.)]\s+')
EMAIL_REGEX = re.compile(r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}')
PHONE_REGEX = re.compile(
    r'(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?',
)
SSN_REGEX = re.compile(
    r'(?!219-09-9999|078-05-1120)(?!666|000|9\d{2})\d{3}-(?!00)\d{2}-'
    r'(?!0{4})\d{4}|(?!219099999|078051120)(?!666|000|9\d{2})\d{3}(?!00)'
    r'\d{2}(?!0{4})\d{4}',
)
CREDIT_CARD_REGEX = re.compile(
    r'(4[0-9]{12}(?:[0-9]{3})?|(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|'
    r'2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}|3[47][0-9]{13}|'
    r'3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|'
    r'(?:2131|1800|35\d{3})\d{11})',
)

# Cache the NameDataset instance for efficiency
_NAME_DATASET = None


def get_name_dataset() -> NameDataset:
    global _NAME_DATASET
    if _NAME_DATASET is None:
        _NAME_DATASET = NameDataset()
    return _NAME_DATASET


# Cache default stop words to avoid reloading them every call
_DEFAULT_STOP_WORDS = set(stopwords.words('english'))


# --------------------------
# Decorators
# --------------------------

def _return_empty_string_for_invalid_input(
        func: Callable[..., str],
) -> Callable[..., str]:
    """Return empty string if the input is None or empty/whitespace."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> str:
        # Check for 'input_text' in kwargs or first positional argument
        input_text = kwargs.get('input_text', args[0] if args else None)
        if input_text is None or not str(input_text).strip():
            return ''
        return func(*args, **kwargs)

    return wrapper


def _return_empty_list_or_string_for_invalid_input(
        func: Callable[..., list[str] | str],
) -> Callable[..., list[str] | str]:
    """Return empty list or empty string if the input is invalid."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> list[str] | str:
        input_text = kwargs.get('input_text', args[0] if args else None)
        if input_text is None or not str(input_text).strip():
            return '' if kwargs.get('return_string', False) else []
        return func(*args, **kwargs)

    return wrapper


def _return_empty_list_for_invalid_input(
        func: Callable[..., list[str]],
) -> Callable[..., list[str]]:
    """Return empty list if the input is None or empty."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> list[str]:
        if 'input_text_or_list' in kwargs:
            input_text_or_list = kwargs['input_text_or_list']
        else:
            try:
                input_text_or_list = args[0]
            except IndexError as err:
                logger.exception('No appropriate positional argument is provided.')
                raise err
        if input_text_or_list is None or len(input_text_or_list) == 0:
            return []
        else:
            return func(*args, **kwargs)

    return wrapper


# --------------------------
# String functions (using _return_empty_string_for_invalid_input)
# --------------------------

@_return_empty_string_for_invalid_input
def to_lower(input_text: str) -> str:
    """Convert input text to lower case."""
    return input_text.lower()


@_return_empty_string_for_invalid_input
def to_upper(input_text: str) -> str:
    """Convert input text to upper case."""
    return input_text.upper()


@_return_empty_string_for_invalid_input
def remove_number(input_text: str) -> str:
    """Remove numbers from the input text."""
    return re.sub(r'\d+', '', input_text)


@_return_empty_string_for_invalid_input
def remove_itemized_bullet_and_numbering(input_text: str) -> str:
    """Remove bullets or numbering in itemized input."""
    return ITEMIZED_REGEX.sub(' ', input_text)


@_return_empty_string_for_invalid_input
def remove_url(input_text: str) -> str:
    """Remove URLs from the input text."""
    return URL_REGEX.sub('', input_text)


@_return_empty_string_for_invalid_input
def remove_punctuation(input_text: str, punctuations: str | None = None) -> str:
    """Remove all punctuations from input text."""
    if punctuations is None:
        import string
        punctuations = string.punctuation
    return input_text.translate(str.maketrans('', '', punctuations))


@_return_empty_string_for_invalid_input
def remove_special_character(
        input_text: str,
        special_characters: str | None = None,
) -> str:
    """Remove special characters from the input text."""
    if special_characters is None:
        special_characters = (
            'å¼«¥ª°©ð±§µæ¹¢³¿®ä£'
            '¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿'
            '×÷‐‑‒–—―‖‘’‚‛“”„‟†‡•‣․‥…‰′″‴'
            '‹›‼‽‾⁄⁂⁎⁑⁓⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞'
            '™℠℡ℤℕℝℚℙℂℵℶℷℸ⅀⅁⅂⅃⅄ⅅⅆⅇⅈⅉ'
            '←↑→↓↔↕↖↗↘↙↚↛↜↝↞↟↠↡↢↣'
            '↤↥↦↧↨↩↪↫↬↭↮↯↰↱↲↳↴↵↶↷↸↹'
        )
    return input_text.translate(str.maketrans('', '', special_characters))


@_return_empty_string_for_invalid_input
def keep_alpha_numeric(input_text: str) -> str:
    """Remove any character except alphanumeric characters."""
    return ''.join(c for c in input_text if c.isalnum())


@_return_empty_string_for_invalid_input
def remove_whitespace(input_text: str, remove_duplicate_whitespace: bool = True) -> str:
    """Remove leading, trailing, and optionally duplicate whitespace."""
    if remove_duplicate_whitespace:
        return ' '.join(re.split(r'\s+', input_text.strip(), flags=re.UNICODE))
    return input_text.strip()


# --------------------------
# Functions that remain list-oriented
# --------------------------

@_return_empty_string_for_invalid_input
def expand_contraction(input_text: str) -> str:
    """Expand contractions in input text."""
    return str(contractions.fix(input_text))


@_return_empty_string_for_invalid_input
def normalize_unicode(input_text: str) -> str:
    """Normalize unicode data to remove accents and umlauts."""
    processed = normalize('NFKD', input_text).encode('ASCII', 'ignore').decode('utf8')
    return processed


@_return_empty_list_for_invalid_input
def remove_stopword(
        input_text_or_list: list[str],
        stop_words: set | None = None,
) -> list[str]:
    """Remove stop words from a list of tokens."""
    if stop_words is None:
        stop_words = _DEFAULT_STOP_WORDS
    if isinstance(stop_words, list):
        stop_words = set(stop_words)
    if isinstance(input_text_or_list, str):
        tokens = word_tokenize(input_text_or_list)
        processed_tokens = [token for token in tokens if token not in stop_words]
    else:
        processed_tokens = [
            token for token in input_text_or_list
            if token not in stop_words and token is not None and len(token) > 0
        ]
    return processed_tokens


@_return_empty_string_for_invalid_input
def remove_email(input_text: str) -> str:
    """Remove email addresses from input text."""
    return EMAIL_REGEX.sub('', input_text)


@_return_empty_string_for_invalid_input
def remove_phone_number(input_text: str) -> str:
    """Remove phone numbers from input text."""
    return PHONE_REGEX.sub('', input_text)


@_return_empty_string_for_invalid_input
def remove_ssn(input_text: str) -> str:
    """Remove social security numbers from input text."""
    return SSN_REGEX.sub('', input_text)


@_return_empty_string_for_invalid_input
def remove_credit_card_number(input_text: str) -> str:
    """Remove credit card numbers from input text."""
    return CREDIT_CARD_REGEX.sub('', input_text)


@_return_empty_list_for_invalid_input
def remove_name(input_text_or_list: str | list[str]) -> list[str]:
    """Remove names from input text using the NameDataset."""
    nd = get_name_dataset()  # Cached instance
    try:
        first_names = {name.lower() for name in nd.first_names.keys()}
        last_names = {name.lower() for name in nd.last_names.keys()}
    except Exception as err:
        logger.error('Error accessing name attributes: %s', err)
        first_names, last_names = set(), set()

    tokens = word_tokenize(input_text_or_list) if isinstance(
        input_text_or_list, str,
    ) else input_text_or_list
    processed_tokens = []
    for token in tokens:
        if token.lower() in first_names or token.lower() in last_names:
            logger.debug(f'Removed name token: {token}')
            continue
        processed_tokens.append(token)
    return processed_tokens


def check_spelling(
        input_text_or_list: str | list[str],
        lang: str = 'en',
        ignore_word_file_path: str | Path = IGNORE_SPELLCHECK_WORD_FILE_PATH,
        acronyms: set[str] | None = None,
) -> str:
    """Check and correct spelling in the input."""
    if input_text_or_list is None or len(input_text_or_list) == 0:
        return ''
    spelling_checker = SpellChecker(language=lang, distance=1)
    spelling_checker.word_frequency.load_text_file(ignore_word_file_path)
    if acronyms is None:
        acronyms = {'NASA', 'FBI', 'CIA', 'SQL', 'HTTP', 'HTTPS'}
    if isinstance(input_text_or_list, str):
        tokens = tokenize_word(input_text_or_list.lower())
    else:
        tokens = [token.lower() for token in input_text_or_list if token]
    misspelled = spelling_checker.unknown(tokens)
    corrected_tokens = []
    for token in tokens:
        if token.upper() in acronyms:
            corrected_tokens.append(token)
            continue
        if token in misspelled:
            correction = spelling_checker.correction(token)
            corrected_tokens.append(correction if correction is not None else token)
        else:
            corrected_tokens.append(token)
    return ' '.join(corrected_tokens).strip()


def tokenize_word(input_text: str) -> list[str]:
    """Convert text into a list of word tokens."""
    if input_text is None or len(input_text) == 0:
        return []
    return [str(token) for token in word_tokenize(input_text)]


_PUNKT_SENTENCE_TOKENIZER = PunktSentenceTokenizer()


def tokenize_sentence(input_text: str) -> list[str]:
    """Convert text into a list of sentence tokens."""
    if not input_text:
        return []
    return [
        str(sentence) for sentence
        in _PUNKT_SENTENCE_TOKENIZER.tokenize(input_text)
    ]


@_return_empty_list_for_invalid_input
def stem_word(
        input_text_or_list: list[str],
        stemmer: PorterStemmer | SnowballStemmer | LancasterStemmer | None = None,
) -> list[str]:
    """Stem each token in the input."""
    if stemmer is None:
        stemmer = PorterStemmer()
    if isinstance(input_text_or_list, str):
        tokens = word_tokenize(input_text_or_list)
        processed_tokens = [stemmer.stem(token) for token in tokens]
    else:
        processed_tokens = [
            stemmer.stem(token)
            for token in input_text_or_list
            if token is not None and len(token) > 0
        ]
    return processed_tokens


@_return_empty_list_for_invalid_input
def lemmatize_word(
        input_text_or_list: str | list[str],
        lemmatizer: WordNetLemmatizer | None = None,
) -> list[str]:
    """Lemmatize each token in the input."""
    if lemmatizer is None:
        lemmatizer = WordNetLemmatizer()
    if isinstance(input_text_or_list, str):
        tokens = word_tokenize(input_text_or_list)
        processed_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    else:
        processed_tokens = [
            lemmatizer.lemmatize(token) for token in input_text_or_list if
            token is not None and len(token) > 0
        ]
    return processed_tokens


@_return_empty_list_or_string_for_invalid_input
def preprocess_text(
        input_text: str,
        return_string: bool = False,
) -> list[str] | str:
    """
    Preprocess input text by applying cleaning steps:
      - Expand contractions
      - Normalize unicode
      - Remove URLs and email addresses
      - Remove punctuation
      - Tokenize the text
      - Remove stopwords
      - Apply stemming and lemmatization

    Parameters:
        input_text (str): The text to preprocess.
        return_string (bool): If True, return a single string;
         otherwise, return a list of tokens.
    """
    # Expand contractions and normalize text
    input_text = expand_contraction(input_text)
    input_text = normalize_unicode(input_text)
    input_text = to_lower(input_text)
    input_text = remove_url(input_text)
    input_text = remove_email(input_text)
    input_text = remove_punctuation(input_text)
    input_text = remove_whitespace(input_text)

    # Tokenize and remove stopwords
    tokens: list[str] = word_tokenize(input_text)
    tokens = remove_stopword(tokens)

    # Apply stemming and lemmatization
    tokens = stem_word(tokens)
    tokens = lemmatize_word(tokens)

    if return_string:
        return ' '.join(tokens)
    return tokens


def convert_str_list_to_lower(input_text_list: list[str]) -> list[str]:
    """Convert a list of strings to lower case."""
    return [text.lower() for text in input_text_list]
