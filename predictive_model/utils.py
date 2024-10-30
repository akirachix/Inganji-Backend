from sklearn.preprocessing import LabelEncoder

# Ordinal mappings for 'education_type', as an example:
ordinal_mappings = {
    'education_type': {'Primary': 1, 'Secondary': 2, 'Higher': 3, 'Postgraduate': 4}
}

from sklearn.preprocessing import LabelEncoder

# Initialize label encoders for label-encoded columns with known categories
label_encoders = {
    'family_status': LabelEncoder(),
    'housing_type': LabelEncoder(),
    'occupation_type': LabelEncoder(),
    'status': LabelEncoder()
}

# Fit label encoders with actual categories from training data
label_encoders['family_status'].fit(['Single', 'Married', 'Divorced', 'Widowed', 'Separated'])
label_encoders['housing_type'].fit(['Rent', 'Own', 'Mortgage', 'Other'])
label_encoders['occupation_type'].fit(['IT', 'Healthcare', 'Education', 'Finance', 'Sales', 'Other'])
label_encoders['status'].fit(['Employed', 'Unemployed', 'Retired', 'Student', 'Self-employed'])


def process_function(input_data):
    """
    Cleans and processes the raw input data before further encoding.

    Args:
        input_data (list of dicts): List of dictionaries containing user input data.

    Returns:
        list of dicts: Cleaned list of dictionaries.
    """
    cleaned_data = []
    for entry in input_data:
        cleaned_entry = {}

        for key, value in entry.items():
            if value is None:
                # Replace None values: 0 for numeric columns, 'unknown' for categorical
                if key in ['age', 'employment_duration', 'num_children', 'total_income']:
                    cleaned_entry[key] = 0
                else:
                    cleaned_entry[key] = 'unknown'
            else:
                cleaned_entry[key] = value

        # Add cleaned entry if it's unique (no duplicates)
        if cleaned_entry not in cleaned_data:
            cleaned_data.append(cleaned_entry)

    return cleaned_data

def encode_features(data):
    """
    Encodes the categorical features based on specified encoding type.

    Args:
        data (list of dicts): List of user input dictionaries containing features.

    Returns:
        list of dicts: Data with encoded categorical and binary features.
    """
    encoded_data = []
    for entry in data:
        encoded_entry = {}

        # Ordinal Encoding for 'education_type'
        if 'education_type' in entry:
            encoded_entry['education_type'] = ordinal_mappings['education_type'].get(entry['education_type'], -1)  # Default to -1 for unknown values

        # Binary Encoding for binary categorical columns
        for col in ['owns_car', 'owns_property']:
            if col in entry:
                encoded_entry[col] = 1 if entry[col].lower() == 'yes' else 0

        # Label Encoding for other categorical columns
        for col, le in label_encoders.items():
            if col in entry:
                try:
                    encoded_entry[col] = le.transform([entry[col]])[0]
                except ValueError:
                    encoded_entry[col] = -1

        # Copy numerical columns directly
        for col in ['age', 'employment_duration', 'num_children', 'total_income']:
            if col in entry:
                encoded_entry[col] = entry[col]

        # Avoid duplicates
        if encoded_entry not in encoded_data:
            encoded_data.append(encoded_entry)

    return encoded_data
