from __future__ import annotations

from typing import Any

import pytest
from imblearn.over_sampling import SMOTE
from sklearn.datasets import make_classification
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

from sanruum.constants import BEST_LOG_REG_FILE
from sanruum.constants import BEST_SVM_FILE
from sanruum.constants import PROCESSED_FILE
from sanruum.constants import RANDOM_FOREST_MODEL_FILE
from sanruum.nlp.train_model import evaluate_model
from sanruum.nlp.train_model import load_and_preprocess_data
from sanruum.nlp.train_model import load_model
from sanruum.nlp.train_model import retrain_model_with_new_data
from sanruum.nlp.train_model import save_model
from sanruum.nlp.train_model import train_models

# Global vectorizer initialization
vectorizer = TfidfVectorizer()


@pytest.fixture
def data() -> Any:
    """Fixture to generate synthetic classification data."""
    X, y = make_classification(
        n_samples=100, n_features=10, n_informative=5, random_state=42,
    )
    return train_test_split(X, y, test_size=0.2, random_state=42)


def test_load_and_preprocess_data(data: Any) -> None:
    """Test loading and preprocessing of data."""
    _, X_test, y_test, _ = data

    # Check if the data is loaded properly
    assert X_test.shape[0] == y_test.shape[0], 'Mismatch between features and labels.'

    # Check if TF-IDF vectorizer is being used correctly
    _, X_tfidf, _, _ = load_and_preprocess_data()  # Don't pass vectorizer here
    assert X_tfidf.shape[0] == X_test.shape[0], \
        'Mismatch between original and TF-IDF feature sizes.'


def test_train_models(data: Any) -> None:
    """Test the training of models."""
    X_train, X_test, y_train, y_test = data

    smote = SMOTE(sampling_strategy='auto', random_state=42, k_neighbors=1)
    X_res, y_res = smote.fit_resample(X_train, y_train)

    # Ensure vectorizer is not passed here
    best_models, _, _, _ = train_models(X_res, y_res)

    # Assert that models are trained
    assert (
        best_models['Logistic Regression']
        is not None
    ), 'Logistic Regression model not trained.'
    assert best_models['SVM'] is not None, 'SVM model not trained.'
    assert (
        best_models['Random Forest']
        is not None
    ), 'Random Forest model not trained.'


def test_evaluate_model(data: Any) -> None:
    """Test the evaluation of a trained model."""
    X_train, X_test, y_train, y_test = data

    smote = SMOTE(sampling_strategy='auto', random_state=42, k_neighbors=1)
    X_res, y_res = smote.fit_resample(X_train, y_train)

    best_models, _, _, _ = train_models(X_res, y_res)

    log_reg = best_models['Logistic Regression']
    svm = best_models['SVM']
    rf = best_models['Random Forest']

    # Evaluate models
    try:
        evaluate_model(log_reg, X_test, y_test, 'Logistic Regression')
        evaluate_model(svm, X_test, y_test, 'SVM')
        evaluate_model(rf, X_test, y_test, 'Random Forest')
    except Exception as e:
        pytest.fail(f'Model evaluation failed: {e}')


def test_save_and_load_model() -> None:
    """Test saving and loading a model."""
    log_reg = load_model(BEST_LOG_REG_FILE)
    assert log_reg is None, \
        'Logistic Regression model should not exist before being saved.'

    # Train and save a model
    _, X_tfidf, y, _ = load_and_preprocess_data()  # Don't pass vectorizer here
    smote = SMOTE(sampling_strategy='auto', random_state=42, k_neighbors=1)
    X_res, y_res = smote.fit_resample(X_tfidf, y)

    best_models, _, _, _ = train_models(X_res, y_res)
    save_model(best_models['Logistic Regression'], BEST_LOG_REG_FILE)

    # Now load the saved model
    log_reg = load_model(BEST_LOG_REG_FILE)
    assert log_reg is not None, 'Failed to load Logistic Regression model.'


def test_retrain_model_with_new_data() -> None:
    """Test retraining of models with new data."""
    retrain_model_with_new_data(PROCESSED_FILE, vectorizer)  # pass vectorizer correctly
    # Assert that the model is retrained and saved
    assert load_model(
        BEST_LOG_REG_FILE,
    ) is not None, 'Logistic Regression model not retrained.'
    assert load_model(BEST_SVM_FILE) is not None, 'SVM model not retrained.'
    assert load_model(
        RANDOM_FOREST_MODEL_FILE,
    ) is not None, 'Random Forest model not retrained.'


if __name__ == '__main__':
    pytest.main()
