# from django.db import models

# # class Prediction(models.Model):
# #     """Model to store prediction requests and their results."""
# #     flag_own_car = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')])
# #     flag_own_realty = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')])
# #     cnt_children = models.IntegerField()
# #     amt_income_total = models.FloatField()
# #     name_education_type = models.CharField(max_length=100)
# #     name_family_status = models.CharField(max_length=100)
# #     name_housing_type = models.CharField(max_length=100)
# #     age_in_days = models.IntegerField()
# #     days_employed = models.IntegerField()
# #     occupation_type = models.CharField(max_length=100)
# #     cnt_fam_members = models.IntegerField()
# #     prediction_result = models.IntegerField(null=True)

# #     def __str__(self):
# #         return f"Prediction for {self.code_gender}, Income: {self.amt_income_total}"


# from django.db import models

# class Prediction(models.Model):
#     """Model to store prediction requests and their results."""

#     # Choices for car ownership
#     CAR_OWNERSHIP_CHOICES = [
#         ('Y', 'Yes'),
#         ('N', 'No')
#     ]
    
#     # Choices for realty ownership
#     REALTY_OWNERSHIP_CHOICES = [
#         ('Y', 'Yes'),
#         ('N', 'No')
#     ]
    
#     # Education type choices
#     EDUCATION_TYPE_CHOICES = [
#         ('Secondary / secondary special', 'Secondary / secondary special'),
#         ('Higher education', 'Higher education'),
#         ('Incomplete higher', 'Incomplete higher'),
#         ('Lower secondary', 'Lower secondary'),
#         ('Academic degree', 'Academic degree'),
#     ]
    
#     # Family status choices
#     FAMILY_STATUS_CHOICES = [
#         ('Married', 'Married'),
#         ('Single / not married', 'Single / not married'),
#         ('Civil marriage', 'Civil marriage'),
#         ('Widow', 'Widow'),
#         ('Separated', 'Separated'),
#     ]
    
#     # Housing type choices
#     HOUSING_TYPE_CHOICES = [
#         ('Rented apartment', 'Rented apartment'),
#         ('House / apartment', 'House / apartment'),
#         ('Municipal apartment', 'Municipal apartment'),
#         ('With parents', 'With parents'),
#         ('Co-op apartment', 'Co-op apartment'),
#         ('Office apartment', 'Office apartment'),
#     ]
    
#     # Occupation type choices
#     OCCUPATION_TYPE_CHOICES = [
#         ('Laborers', 'Laborers'),
#         ('Core staff', 'Core staff'),
#         ('Sales staff', 'Sales staff'),
#         ('Managers', 'Managers'),
#         ('Drivers', 'Drivers'),
#         ('High skill tech staff', 'High skill tech staff'),
#         ('Accountants', 'Accountants'),
#         ('Medicine staff', 'Medicine staff'),
#     ]

#     # Fields for the prediction input
#     owns_car = models.CharField(max_length=1, choices=CAR_OWNERSHIP_CHOICES)
#     owns_property = models.CharField(max_length=1, choices=REALTY_OWNERSHIP_CHOICES)
#     num_children = models.IntegerField()
#     total_income = models.FloatField()
#     education_type = models.CharField(max_length=100, choices=EDUCATION_TYPE_CHOICES)
#     family_status = models.CharField(max_length=100, choices=FAMILY_STATUS_CHOICES)
#     housing_type = models.CharField(max_length=100, choices=HOUSING_TYPE_CHOICES)
#     age = models.IntegerField()
#     employment_duration = models.IntegerField()  # Adjusted to Integer for employment duration
#     occupation_type = models.CharField(max_length=100, choices=OCCUPATION_TYPE_CHOICES)
#     number_of_family_members = models.IntegerField()
#     total_dependents = models.IntegerField()  # Include this field
#     household_size = models.IntegerField()  # Include this field
#     is_long_employment = models.BooleanField()  # Boolean field for long employment
#     prediction_result = models.IntegerField(null=True)  # Field to store prediction result



# from django.db import models

# class Prediction(models.Model):
#     """Model to store prediction requests and their results."""

#     # Choices for car ownership
#     CAR_OWNERSHIP_CHOICES = [
#         ('Y', 'Yes'),
#         ('N', 'No')
#     ]
    
#     # Choices for realty ownership
#     REALTY_OWNERSHIP_CHOICES = [
#         ('Y', 'Yes'),
#         ('N', 'No')
#     ]
    
#     # Education type choices
#     EDUCATION_TYPE_CHOICES = [
#         ('Lower secondary', 'Lower secondary'),
#         ('Secondary / secondary special', 'Secondary / secondary special'),
#         ('Higher education', 'Higher education'),
#         ('Incomplete higher', 'Incomplete higher'),
#         ('Academic degree', 'Academic degree'),
#     ]
    
#     # Family status choices
#     FAMILY_STATUS_CHOICES = [
#         ('Single / not married', 'Single / not married'),
#         ('Married', 'Married'),
#         ('Civil marriage', 'Civil marriage'),
#         ('Widow', 'Widow'),
#         ('Separated', 'Separated'),
#     ]
    
#     # Housing type choices
#     HOUSING_TYPE_CHOICES = [
#         ('Rented apartment', 'Rented apartment'),
#         ('House / apartment', 'House / apartment'),
#         ('Municipal apartment', 'Municipal apartment'),
#         ('With parents', 'With parents'),
#         ('Co-op apartment', 'Co-op apartment'),
#         ('Office apartment', 'Office apartment'),
#     ]
    
#     # Occupation type choices
#     OCCUPATION_TYPE_CHOICES = [
#         ('Laborers', 'Laborers'),
#         ('Core staff', 'Core staff'),
#         ('Sales staff', 'Sales staff'),
#         ('Managers', 'Managers'),
#         ('Drivers', 'Drivers'),
#         ('High skill tech staff', 'High skill tech staff'),
#         ('Accountants', 'Accountants'),
#         ('Medicine staff', 'Medicine staff'),
#     ]

#     # Fields for the prediction input
#     owns_car = models.CharField(
#         max_length=1, 
#         choices=CAR_OWNERSHIP_CHOICES,
#         verbose_name='Car Ownership',
#         help_text='Select Y for Yes or N for No.'
#     )
    
#     owns_property = models.CharField(
#         max_length=1, 
#         choices=REALTY_OWNERSHIP_CHOICES,
#         verbose_name='Property Ownership',
#         help_text='Select Y for Yes or N for No.'
#     )
    
#     num_children = models.IntegerField(
#         verbose_name='Number of Children',
#         help_text='Enter the number of children.'
#     )
    
#     total_income = models.FloatField(
#         verbose_name='Total Income',
#         help_text='Enter your total income.'
#     )
    
#     education_type = models.CharField(
#         max_length=100, 
#         choices=EDUCATION_TYPE_CHOICES,
#         verbose_name='Education Level',
#         help_text='Select your highest education level.'
#     )
    
#     family_status = models.CharField(
#         max_length=100, 
#         choices=FAMILY_STATUS_CHOICES,
#         verbose_name='Family Status',
#         help_text='Select your current family status.'
#     )
    
#     housing_type = models.CharField(
#         max_length=100, 
#         choices=HOUSING_TYPE_CHOICES,
#         verbose_name='Housing Type',
#         help_text='Select your type of housing.'
#     )
    
#     age = models.IntegerField(
#         verbose_name='Age',
#         help_text='Enter your age.'
#     )
    
#     employment_duration = models.IntegerField(
#         verbose_name='Employment Duration (Months)', 
#         help_text='Enter the duration of employment in months.'
#     )
    
#     occupation_type = models.CharField(
#         max_length=100, 
#         choices=OCCUPATION_TYPE_CHOICES,
#         verbose_name='Occupation',
#         help_text='Select your occupation.'
#     )
    
#     number_of_family_members = models.IntegerField(
#         verbose_name='Number of Family Members',
#         help_text='Enter the total number of family members.'
#     )
    
#     total_dependents = models.IntegerField(
#         verbose_name='Total Dependents',
#         help_text='Enter the number of dependents.'
#     )
    
#     household_size = models.IntegerField(
#         verbose_name='Household Size',
#         help_text='Enter the size of your household.'
#     )
    
#     is_long_employment = models.BooleanField(
#         verbose_name='Long-term Employment',
#         help_text='Indicate if employed for a long duration.'
#     )
    
#     prediction_result = models.IntegerField(
#         verbose_name='Prediction Result',
#         help_text='Result of the prediction: 1 for Eligible, 0 for Not Eligible.'
#     )

#     def __str__(self):
#         return f"Prediction for {self.total_income} income - {self.prediction_result}"



from django.db import models

class Prediction(models.Model):
    """Model to store prediction requests and their results."""

    # Choices for car ownership
    CAR_OWNERSHIP_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No')
    ]
    
    # Choices for realty ownership
    REALTY_OWNERSHIP_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No')
    ]
    
    # Education type choices
    EDUCATION_TYPE_CHOICES = [
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
        ('Higher', 'Higher'),
        ('Postgraduate', 'Postgraduate'),
    ]
    
    # Family status choices
    FAMILY_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
        ('Separated', 'Separated'),
    ]
    
    # Housing type choices
    HOUSING_TYPE_CHOICES = [
        ('Rent', 'Rent'),
        ('Own', 'Own'),
        ('Mortgage', 'Mortgage'),
        ('Other', 'Other'),
    ]

    # Fields for the prediction input
    owns_car = models.CharField(
        max_length=1, 
        choices=CAR_OWNERSHIP_CHOICES,
        verbose_name='Car Ownership',
        help_text='Select Y for Yes or N for No.'
    )
    
    owns_property = models.CharField(
        max_length=1, 
        choices=REALTY_OWNERSHIP_CHOICES,
        verbose_name='Property Ownership',
        help_text='Select Y for Yes or N for No.'
    )
    
    num_children = models.IntegerField(
        verbose_name='Number of Children',
        help_text='Enter the number of children.'
    )
    
    total_income = models.FloatField(
        verbose_name='Total Income',
        help_text='Enter your total income.'
    )
    
    education_type = models.CharField(
        max_length=100, 
        choices=EDUCATION_TYPE_CHOICES,
        verbose_name='Education Level',
        help_text='Select your highest education level.'
    )
    
    family_status = models.CharField(
        max_length=100, 
        choices=FAMILY_STATUS_CHOICES,
        verbose_name='Family Status',
        help_text='Select your current family status.'
    )
    
    housing_type = models.CharField(
        max_length=100, 
        choices=HOUSING_TYPE_CHOICES,
        verbose_name='Housing Type',
        help_text='Select your type of housing.'
    )
    
    age = models.IntegerField(
        verbose_name='Age',
        help_text='Enter your age.'
    )
    
    employment_duration = models.IntegerField(
        verbose_name='Employment Duration (Months)', 
        help_text='Enter the duration of employment in months.'
    )
    
    number_of_family_members = models.IntegerField(
        verbose_name='Number of Family Members',
        help_text='Enter the total number of family members.'
    )
    
    total_dependents = models.IntegerField(
        verbose_name='Total Dependents',
        help_text='Enter the total number of dependents.'
    )
    
    is_long_employment = models.BooleanField(
        verbose_name='Long-term Employment',
        help_text='Select if you have long-term employment.'
    )
    
    prediction_result = models.IntegerField(
        null=True, 
        verbose_name='Prediction Result',
        help_text='Stores the result of the prediction.'
    )
    
    def __str__(self):
        return f"Prediction(id={self.id}, Result={self.prediction_result})"
