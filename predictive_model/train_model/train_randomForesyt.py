
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



import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from predictive_model.utils import process_function, encode_features


def train_random_forest_model(data, target_col, model_path="model/trained_rf_model.pkl"):
    """
    Trains a RandomForestClassifier on the given data and saves it.

    Args:
        data (list of dicts): Preprocessed and encoded training data.
        target_col (str): Target variable column name.
        model_path (str): Path to save the trained model.

    Returns:
        None
    """
    # Define features
    features = [
        'owns_car', 'owns_property', 'num_children', 'total_income', 
        'education_type', 'family_status', 'housing_type', 'age', 
        'employment_duration', 'occupation_type', 'number_of_family_members'
    ]
    
    # Convert data to pandas DataFrame
    import pandas as pd
    data_df = pd.DataFrame(data)
    
    # Extract features and target variable
    X = data_df[features]
    y = data_df[target_col]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize RandomForest model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print(f'Training Accuracy: {model.score(X_train, y_train):.2f}')
    print(f'Test Accuracy: {accuracy:.2f}')

    # Save the trained model
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    # Load data (assuming data is a list of dicts)
    raw_data = [...]  # Load or input raw data here
    target_col = "label"

    # Process and encode data
    processed_data = process_function(raw_data)
    encoded_data = encode_features(processed_data)

    # Train and save model
    train_random_forest_model(encoded_data, target_col)
