from __future__ import annotations

import os
from typing import Any

import joblib
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import auc
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from sanruum.constants import BEST_LOG_REG_FILE
from sanruum.constants import BEST_SVM_FILE
from sanruum.constants import MODEL_DIR
from sanruum.constants import RANDOM_FOREST_MODEL_FILE
from sanruum.constants import RAW_DATA_FILE

matplotlib.use('Agg')


def save_model(model: Any, filename: str) -> None:
    """Save model to disk."""
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    filepath = os.path.join(MODEL_DIR, filename)
    joblib.dump(model, filepath)
    print(f'Model saved to: {filepath}')


def load_model(filename: str) -> Any | None:
    """Load model from disk."""
    filepath = os.path.join(MODEL_DIR, filename)
    if os.path.exists(filepath):
        return joblib.load(filepath)
    else:
        print(f'Model file not found: {filepath}')
        return None


def evaluate_model(model: Any, X_test: Any, y_test: Any, model_name: str) -> None:
    """Evaluate model performance and save ROC curve."""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'{model_name} Accuracy: {accuracy:.4f}')
    print(classification_report(y_test, y_pred))
    print(f'Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}')

    # ROC Curve and AUC
    if hasattr(model, 'predict_proba'):
        y_prob = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)

        plt.figure()
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC Curve - {model_name}')
        plt.legend(loc='lower right')

        # Save ROC curve
        roc_filename = os.path.join(MODEL_DIR, f'roc_curve_{model_name}.png')
        plt.savefig(roc_filename)
        print(f'ROC curve saved: {roc_filename}')
        plt.close()


def load_and_preprocess_data() -> tuple[pd.DataFrame, Any, Any, TfidfVectorizer]:
    """Load and preprocess data."""
    data = pd.read_csv(RAW_DATA_FILE)
    # Drop rows with missing 'text' or 'label'
    data.dropna(subset=['text', 'label'], inplace=True)
    X = data['text']
    y = data['label']

    # Convert text to numerical features using TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(
        stop_words='english', max_df=0.9, min_df=2, ngram_range=(1, 2),
    )
    X_tfidf = vectorizer.fit_transform(X)

    return data, X_tfidf, y, vectorizer


def train_models(
        X_train: Any, y_train: Any,
) -> tuple[dict[str, Any], GridSearchCV, GridSearchCV, GridSearchCV]:
    """Train models using hyperparameter tuning."""
    stratified_kfold = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

    # Logistic Regression
    log_reg_param_grid = {
        'C': [0.1, 1, 10], 'penalty': [
            'l2',
        ], 'solver': ['liblinear', 'saga'],
    }
    grid_search_log_reg = GridSearchCV(
        estimator=LogisticRegression(max_iter=200), param_grid=log_reg_param_grid,
        cv=stratified_kfold, n_jobs=-1, verbose=1,
    )
    grid_search_log_reg.fit(X_train, y_train)

    # SVM
    svm_param_grid = {
        'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf'],
    }
    grid_search_svm = GridSearchCV(
        SVC(probability=True),
        svm_param_grid,
        cv=stratified_kfold,
        n_jobs=-1,
        verbose=1,
    )
    grid_search_svm.fit(X_train, y_train)

    # Random Forest
    rf_param_grid = {'n_estimators': [100, 200, 300], 'max_depth': [10, 20, 30, None]}
    grid_search_rf = GridSearchCV(
        RandomForestClassifier(random_state=42), rf_param_grid, cv=stratified_kfold,
        n_jobs=-1, verbose=1,
    )
    grid_search_rf.fit(X_train, y_train)

    best_log_reg = grid_search_log_reg.best_estimator_
    best_svm = grid_search_svm.best_estimator_
    best_rf = grid_search_rf.best_estimator_

    return {
        'Logistic Regression': best_log_reg, 'SVM': best_svm,
        'Random Forest': best_rf,
    }, grid_search_log_reg, grid_search_svm, grid_search_rf


def retrain_model_with_new_data(
        new_data_file: str, vectorizer: TfidfVectorizer,
) -> None:
    """Retrain models with new data."""
    if not os.path.exists(new_data_file):
        print(f'Error: Data file not found: {new_data_file}')
        return

    data = pd.read_csv(new_data_file)
    if data.isnull().sum().any():
        print('Warning: Missing values detected in new data. Consider preprocessing.')

    X_new = data['text']
    y_new = data['label']

    # Use existing vectorizer (DO NOT FIT AGAIN)
    X_new_tfidf = vectorizer.transform(X_new)

    smote = SMOTE(sampling_strategy='auto', random_state=42, k_neighbors=1)
    X_res_new, y_res_new = smote.fit_resample(X_new_tfidf, y_new)

    log_reg = load_model(BEST_LOG_REG_FILE) or LogisticRegression(max_iter=1000)
    svm = load_model(BEST_SVM_FILE) or SVC(probability=True)
    rf = load_model(RANDOM_FOREST_MODEL_FILE) or RandomForestClassifier(
        n_estimators=100, random_state=42,
        class_weight='balanced',
    )

    log_reg.fit(X_res_new, y_res_new)
    svm.fit(X_res_new, y_res_new)
    rf.fit(X_res_new, y_res_new)

    # Save updated models
    save_model(log_reg, BEST_LOG_REG_FILE)
    save_model(svm, BEST_SVM_FILE)
    save_model(rf, RANDOM_FOREST_MODEL_FILE)

    print('Models retrained and saved successfully.')


def main() -> None:
    # Load and preprocess data
    _, X_tfidf, y, vectorizer = load_and_preprocess_data()

    # Train models and get best models
    X_train, X_test, y_train, y_test = train_test_split(
        X_tfidf, y, test_size=0.2, random_state=42, stratify=y,
    )
    smote = SMOTE(sampling_strategy='auto', random_state=42, k_neighbors=1)
    X_res, y_res = smote.fit_resample(X_train, y_train)

    best_models, grid_search_log_reg, grid_search_svm, grid_search_rf = train_models(
        X_res, y_res,
    )

    # Save best models
    save_model(best_models['Logistic Regression'], BEST_LOG_REG_FILE)
    save_model(best_models['SVM'], BEST_SVM_FILE)
    save_model(best_models['Random Forest'], RANDOM_FOREST_MODEL_FILE)

    # Load models for later use
    loaded_log_reg = load_model(BEST_LOG_REG_FILE)
    loaded_svm = load_model(BEST_SVM_FILE)
    loaded_rf = load_model(RANDOM_FOREST_MODEL_FILE)

    # Evaluate best models
    print('Logistic Regression Evaluation:')
    evaluate_model(loaded_log_reg, X_test, y_test, 'Logistic Regression')

    print('SVM Evaluation:')
    evaluate_model(loaded_svm, X_test, y_test, 'SVM')

    print('Random Forest Evaluation:')
    evaluate_model(loaded_rf, X_test, y_test, 'Random Forest')


if __name__ == '__main__':
    main()
