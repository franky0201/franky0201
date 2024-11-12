import numpy as np
import pandas as pd
from sklearn.model_selection import cross_validate, StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

# Load dataset
data_path = 'C:/Users/Administrator/Downloads/breast+cancer+wisconsin+diagnostic/wdbc.data'
column_names = ["ID", "Diagnosis"] + [f"feature_{i}" for i in range(1, 31)]
data = pd.read_csv(data_path, header=None, names=column_names)

# Drop ID column and encode Diagnosis column
data = data.drop(columns=["ID"])
data['Diagnosis'] = data['Diagnosis'].map({'M': 1, 'B': 0})

# Split features and target
X = data.drop(columns=["Diagnosis"])
y = data["Diagnosis"]

# Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Define the model
xgb_model = XGBClassifier(random_state=42)

# Define parameter grid for XGBoost
param_grid = {
    'n_estimators': [200, 300, 400],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7],
    'subsample': [0.7, 0.8, 1.0],
    'colsample_bytree': [0.7, 0.8, 1.0]
}

# Grid search with stratified cross-validation
grid_search = GridSearchCV(
    xgb_model, param_grid, cv=StratifiedKFold(n_splits=5), return_train_score=True
)
grid_search.fit(X_scaled, y)
best_model = grid_search.best_estimator_

# Evaluate the model with cross-validation
cv_results = cross_validate(best_model, X_scaled, y, cv=5, return_train_score=True)

# Calculate accuracy
acc_train = np.mean(cv_results['train_score'])
acc_test = np.mean(cv_results['test_score'])
print(f'* Accuracy @ training data: {acc_train:.3f}')
print(f'* Accuracy @ test data: {acc_test:.3f}')
print(f'* Your score: {max(10 + 100 * (acc_test - 0.9), 0):.0f}')
