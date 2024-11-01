
# import pandas as pd
# from imblearn.over_sampling import SMOTE
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
# import joblib
# from django_churn_model_app.utils import load_and_merge_data, preprocess_data, encode_features

# def handle_class_imbalance(X, y):
#     smote = SMOTE(random_state=42)
#     X_res, y_res = smote.fit_resample(X, y)
#     return X_res, y_res

# def train_random_forest_model(X_train, y_train):
#     rf_model = RandomForestClassifier(random_state=42)
#     rf_model.fit(X_train, y_train)
#     return rf_model

# def evaluate_model(model, X_test, y_test):
#     y_pred = model.predict(X_test)
#     accuracy = accuracy_score(y_test, y_pred)
#     print(f"Model Accuracy: {accuracy * 100:.2f}%")
#     print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
#     print("Classification Report:\n", classification_report(y_test, y_pred))
#     return accuracy

# def save_model(model, model_path="model/trained_rf_model.pkl"):
#     joblib.dump(model, model_path)
#     print(f"Model saved to {model_path}")

# def main():
#     file1 = "/home/student/Machine Learning/application_record.csv"
#     file2 = "/home/student/Machine Learning/credit_record.csv"
#     merge_column = "ID"

#     merged_df = load_and_merge_data(file1, file2, merge_column)

#     processed_data = preprocess_data(merged_df)

#     features = [
#                 'owns_car', 'owns_property', 'num_children', 'total_income', 
#                 'education_type', 'family_status', 'housing_type', 'age', 
#                 'employment_duration', 'occupation_type', 'number_of_family_members'
#             ]
#     target = 'label'

#     X = processed_data[features]
#     y = processed_data[target]

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     X_train_sm, y_train_sm = handle_class_imbalance(X_train, y_train)

#     rf_model = train_random_forest_model(X_train_sm, y_train_sm)

#     evaluate_model(rf_model, X_test, y_test)

#     save_model(rf_model)

# if __name__ == "__main__":
#     main()


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

    # Prepare the feature matrix (X) and the target vector (y)
    X = [[data[feature] for feature in features] for data in cleaned_data]
    y = [data['label'] for data in cleaned_data]

    # Apply SMOTE to handle class imbalance
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled)

    # Initialize the Random Forest model
    model = RandomForestClassifier(random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Test Accuracy: {accuracy:.2f}')
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Save the model
    model_path = os.path.join(os.path.dirname(__file__), 'rForest_model.pkl')
    with open(model_path, "wb") as file:
        pickle.dump(model, file)
    print("Model saved successfully!")

if __name__ == "__main__":
    # Placeholder for cleaned user input data
    cleaned_data = []  # Replace with actual cleaned data loading or creation
    train_random_forest_model(cleaned_data)
