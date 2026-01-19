import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, precision_score
import joblib

# Generate synthetic data
np.random.seed(42)
n_samples = 10000
lst = np.random.uniform(20, 40, n_samples)  # LST in Celsius
ndvi = np.random.uniform(0.1, 0.9, n_samples)
rainfall = np.random.uniform(0, 50, n_samples)  # mm

# Feature engineering
X1 = lst * ndvi
X2 = np.sqrt(lst**2 + ndvi**2)
epsilon = 1e-6
X3 = np.log(1 + ndvi / (rainfall + epsilon))

X = np.column_stack([lst, ndvi, rainfall, X1, X2, X3])

# Target: fire if LST > 35 and NDVI < 0.3 and rainfall < 10, with some noise
y = ((lst > 35) & (ndvi < 0.3) & (rainfall < 10)).astype(int)
# Add some noise to make it realistic
noise = np.random.rand(n_samples) < 0.1
y[noise] = 1 - y[noise]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Models with strict regularization
rf = RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_split=10, random_state=42)
xgb = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.01, reg_alpha=1, reg_lambda=1, random_state=42)
meta = LogisticRegression(C=0.1, random_state=42)

stacking = StackingClassifier(estimators=[('rf', rf), ('xgb', xgb)], final_estimator=meta, cv=5)

# Train
stacking.fit(X_train, y_train)

# Evaluate
y_pred = stacking.predict(X_test)
recall = recall_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
print(f'Recall: {recall:.2f}, Precision: {precision:.2f}')

# Save model
joblib.dump(stacking, 'model.pkl')
