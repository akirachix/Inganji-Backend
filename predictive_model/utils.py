
from sklearn.preprocessing import LabelEncoder

ordinal_mappings = {
    'education_type': {
        'Primary': 1,
        'Secondary': 2,
        'Higher': 3,
        'Postgraduate': 4
    }
}

label_encoders = {
    'family_status': LabelEncoder(),
    'housing_type': LabelEncoder(),
    'occupation_type': LabelEncoder(),
    'status': LabelEncoder()
}

label_encoders['family_status'].fit(['Single', 'Married', 'Divorced', 'Widowed', 'Separated'])
label_encoders['housing_type'].fit(['Rent', 'Own', 'Mortgage', 'Other'])
label_encoders['occupation_type'].fit(['IT', 'Healthcare', 'Education', 'Finance', 'Sales', 'Other'])
label_encoders['status'].fit(['Employed', 'Unemployed', 'Retired', 'Student', 'Self-employed'])

def encode_features(data):
  
    encoded_data = []
    for entry in data:
        encoded_entry = {}

        encoded_entry['age'] = entry.get('age', -1)
        encoded_entry['education_type'] = ordinal_mappings['education_type'].get(entry.get('education_type'), -1)
        encoded_entry['employment_duration'] = entry.get('employment_duration', -1)
        encoded_entry['num_children'] = entry.get('num_children', 0)
        encoded_entry['total_income'] = entry.get('total_income', 0.0)
        encoded_entry['number_of_family_members'] = entry.get('number_of_family_members', 0)
        encoded_entry['total_dependents'] = entry.get('total_dependents', 0)
        encoded_entry['household_size'] = entry.get('household_size', 0)

        encoded_entry['family_status'] = label_encoders['family_status'].transform([entry.get('family_status', 'unknown')])[0]
        encoded_entry['housing_type'] = label_encoders['housing_type'].transform([entry.get('housing_type', 'unknown')])[0]
        encoded_entry['occupation_type'] = label_encoders['occupation_type'].transform([entry.get('occupation_type', 'unknown')])[0]

        for col in ['owns_car', 'owns_property', 'is_long_employment']:
            encoded_entry[col] = 1 if entry.get(col, 'no').lower() == 'yes' else 0
        
        encoded_data.append(encoded_entry)

    return encoded_data


def process_function(user_input):
    
    encoded_input = encode_features(user_input)
    return encoded_input
