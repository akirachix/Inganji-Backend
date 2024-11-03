

import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE

def train_random_forest_model(cleaned_data):
    features = [
        'owns_car', 'owns_property', 'num_children', 'total_income',
        'education_type', 'family_status', 'housing_type', 'age', 
        'employment_duration', 'occupation_type', 'number_of_family_members',
        'total_dependents', 'household_size', 'is_long_employment'
    ]

    X = [[data[feature] for feature in features] for data in cleaned_data]
    y = [data['label'] for data in cleaned_data]

    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled)

    model = RandomForestClassifier(random_state=42)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Test Accuracy: {accuracy:.2f}')
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    model_path = os.path.join(os.path.dirname(__file__), 'rForest_model.pkl')
    with open(model_path, "wb") as file:
        pickle.dump(model, file)
    print("Model saved successfully!")

if __name__ == "__main__":
    cleaned_data = []
    train_random_forest_model(cleaned_data)
