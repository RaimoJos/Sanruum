import json
import os

import joblib
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.svm import SVC

from sanruum.constants import RAW_DATA_FILE, MODEL_DIR, PARAMS_FILE, BEST_LOG_REG_FILE, BEST_SVM_FILE, \
    RANDOM_FOREST_MODEL_FILE

matplotlib.use('Agg')


def save_model(model, filename):
    filepath = os.path.join(MODEL_DIR, filename)
    joblib.dump(model, filepath)
    print(f"Model saved to: {filepath}")


def load_model(filename):
    filepath = os.path.join(MODEL_DIR, filename)
    if os.path.exists(filepath):
        return joblib.load(filepath)
    else:
        print(f"Model file not found: {filepath}")
        return None


# Evaluation function
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{model.__class__.__name__} Accuracy: {accuracy:.4f}")
    print(classification_report(y_test, y_pred))
    print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")

    # ROC Curve and AUC
    if hasattr(model, 'predict_proba'):  # Check if model supports probability predictions
        y_prob = model.predict_proba(X_test)[:, 1]
        fpr, tpr, thresholds = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)

        # Plot ROC curve
        plt.figure()
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC)')
        plt.legend(loc='lower right')
        plt.show()


# Load your dataset
data = pd.read_csv(RAW_DATA_FILE)
# Check for missing values
print("Missing values in the dataset:", data.isnull().sum())

# Drop rows with missing values in 'text' or 'label'
data.dropna(subset=['text', 'label'], inplace=True)

X = data['text']  # Feature column (text)
y = data['label']  # Target column (label)

# Convert text to numerical features using TF-IDF Vectorizer
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.9, min_df=2, ngram_range=(1, 2))
X_tfidf = vectorizer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42, stratify=y)

# Apply SMOTE only to training data
smote = SMOTE(sampling_strategy='auto', random_state=42, k_neighbors=1)
X_res, y_res = smote.fit_resample(X_train, y_train)

print(f"Resampled X_train shape: {X_res.shape}, y_train shape: {y_res.shape}")  # Verify the resampling

# Cross-validation setup
stratified_kfold = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

# Models definition
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "SVM": SVC(probability=True),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
}

# Hyperparameter tuning with GridSearchCV (Logistic Regression)
log_reg_param_grid = {
    'C': [0.1, 1, 10],
    'penalty': ['l2'],
    'solver': ['liblinear', 'saga'],
}
grid_search_log_reg = GridSearchCV(estimator=LogisticRegression(max_iter=200), param_grid=log_reg_param_grid,
                                   cv=stratified_kfold, n_jobs=-1, verbose=1)
grid_search_log_reg.fit(X_res, y_res)
best_log_reg = grid_search_log_reg.best_estimator_

# Hyperparameter tuning with GridSearchCV (SVM)
svm_param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'rbf'],
}
grid_search_svm = GridSearchCV(SVC(probability=True), svm_param_grid, cv=stratified_kfold, n_jobs=-1, verbose=1)
grid_search_svm.fit(X_res, y_res)
best_svm = grid_search_svm.best_estimator_

# Hyperparameter tuning for Random Forest (only the 'n_estimators' and 'max_depth' hyperparameters)
rf_param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30, None],
}

grid_search_rf = GridSearchCV(RandomForestClassifier(random_state=42), rf_param_grid, cv=stratified_kfold, n_jobs=-1,
                              verbose=1)
grid_search_rf.fit(X_res, y_res)
best_rf = grid_search_rf.best_estimator_

# Fit the best models
best_log_reg.fit(X_res, y_res)
best_svm.fit(X_res, y_res)
best_rf.fit(X_res, y_res)

# Save models
save_model(best_log_reg, BEST_LOG_REG_FILE)
save_model(best_svm, BEST_SVM_FILE)
save_model(best_rf, RANDOM_FOREST_MODEL_FILE)

# Load models for later use
loaded_log_reg = load_model(BEST_LOG_REG_FILE)
loaded_svm = load_model(BEST_SVM_FILE)
loaded_rf = load_model(RANDOM_FOREST_MODEL_FILE)

if loaded_log_reg:
    print("Loaded Logistic Regression Model")
if loaded_svm:
    print("Loaded SVM Model")
if loaded_rf:
    print("Loaded Random Forest Model")

# Evaluate the Best Models
print("Logistic Regression Evaluation:")
evaluate_model(best_log_reg, X_test, y_test)

print("SVM Evaluation:")
evaluate_model(best_svm, X_test, y_test)

print("Random Forest Evaluation:")
evaluate_model(best_rf, X_test, y_test)

# Save the ROC curve
plt.savefig('output.png')  # Save to a file
plt.close()


# Save best parameters to a file
def save_best_params(params):
    with open(PARAMS_FILE, 'w') as f:
        json.dump(params, f)


# Load best parameters from a file
def load_best_params():
    if os.path.exists(PARAMS_FILE):
        with open(PARAMS_FILE, "r") as f:
            return json.load(f)
    return {}


# Function to allow the model to retrain with new data
def retrain_model(new_data_file):
    data = pd.read_csv(new_data_file)
    X_new = data['text']
    y_new = data['label']
    X_new_tfidf = vectorizer.transform(X_new)
    X_res_new, y_res_new = smote.fit_resample(X_new_tfidf, y_new)

    # Retrain models with new data
    best_log_reg.fit(X_res_new, y_res_new)
    best_svm.fit(X_res_new, y_res_new)
    best_rf.fit(X_res_new, y_res_new)

    # Save the newly trained models
    save_model(best_log_reg, BEST_LOG_REG_FILE)
    save_model(best_svm, BEST_SVM_FILE)
    save_model(best_rf, RANDOM_FOREST_MODEL_FILE)


# To retrain the model with new data, call this function periodically or when new data is available
# retrain_model('path_to_new_data.csv')

# Predict with the updated models
print("Logistic Regression Prediction:", best_log_reg.predict(X_test))
print("SVM Prediction:", best_svm.predict(X_test))
print("Random Forest Prediction:", best_rf.predict(X_test))

# Save TF-IDF matrix shape for verification
print(f"TF-IDF matrix shape: {X_tfidf.shape}")  # Check the shape of the matrix
