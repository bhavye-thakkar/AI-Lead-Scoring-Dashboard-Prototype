# train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from xgboost import XGBClassifier
import joblib

# Load data
df = pd.read_csv("lead_data.csv")

# Create target variable (synthetic)
conditions = [
    (df['credit_score'] > 700) & (df['income'] > 500000),
    (df['prior_inquiries'] > 5) & (df['comments'].str.contains('urgent|asap', case=False))
]
choices = [1, 1]
df['high_intent'] = np.select(conditions, choices, default=0)

# Preprocessing
categorical_features = ['age_group', 'family_background', 'employment_status', 'property_type', 'location_tier']
preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(), categorical_features)],
    remainder='passthrough'
)

X = df.drop(['phone_number', 'email', 'comments', 'high_intent'], axis=1)
y = df['high_intent']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocess and train
X_processed = preprocessor.fit_transform(X_train)
model = XGBClassifier()
model.fit(X_processed, y_train)

# Save artifacts
joblib.dump(model, 'lead_model.pkl')
joblib.dump(preprocessor, 'preprocessor.pkl')