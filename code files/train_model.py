import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv('dataset/Crop_recommendation.csv')
print(f'Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns')

# Encode target
le = LabelEncoder()
df['crop_encoded'] = le.fit_transform(df['label'])

# Features and target
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['crop_encoded']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train models
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'KNN': KNeighborsClassifier(n_neighbors=5),
    'Decision Tree': DecisionTreeClassifier(random_state=42)
}

best_acc = 0
best_name = ''
for name, m in models.items():
    m.fit(X_train_scaled, y_train)
    acc = accuracy_score(y_test, m.predict(X_test_scaled))
    print(f'{name}: {acc:.4f}')
    if acc > best_acc:
        best_acc = acc
        best_name = name

print(f'\nBest model: {best_name} ({best_acc:.4f})')

# Save best model
model_data = {
    'model': models[best_name],
    'label_encoder': le,
    'scaler': scaler,
    'model_name': best_name
}
with open('app/model.pkl', 'wb') as f:
    pickle.dump(model_data, f)
print('Model saved to app/model.pkl')

# Verify
with open('app/model.pkl', 'rb') as f:
    loaded = pickle.load(f)
test_pred = loaded['model'].predict(loaded['scaler'].transform(X_test.iloc[0:1]))
predicted_crop = loaded['label_encoder'].inverse_transform(test_pred)[0]
actual_crop = loaded['label_encoder'].inverse_transform([y_test.iloc[0]])[0]
print(f'Verification - Predicted: {predicted_crop}, Actual: {actual_crop}')
print('Done!')
