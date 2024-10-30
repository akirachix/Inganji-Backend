from django.db import models

# class Prediction(models.Model):
#     """Model to store prediction requests and their results."""
#     flag_own_car = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')])
#     flag_own_realty = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')])
#     cnt_children = models.IntegerField()
#     amt_income_total = models.FloatField()
#     name_education_type = models.CharField(max_length=100)
#     name_family_status = models.CharField(max_length=100)
#     name_housing_type = models.CharField(max_length=100)
#     age_in_days = models.IntegerField()
#     days_employed = models.IntegerField()
#     occupation_type = models.CharField(max_length=100)
#     cnt_fam_members = models.IntegerField()
#     prediction_result = models.IntegerField(null=True)

#     def __str__(self):
#         return f"Prediction for {self.code_gender}, Income: {self.amt_income_total}"


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
        ('Secondary / secondary special', 'Secondary / secondary special'),
        ('Higher education', 'Higher education'),
        ('Incomplete higher', 'Incomplete higher'),
        ('Lower secondary', 'Lower secondary'),
        ('Academic degree', 'Academic degree'),
    ]
    
    # Family status choices
    FAMILY_STATUS_CHOICES = [
        ('Married', 'Married'),
        ('Single / not married', 'Single / not married'),
        ('Civil marriage', 'Civil marriage'),
        ('Widow', 'Widow'),
        ('Separated', 'Separated'),
    ]
    
    # Housing type choices
    HOUSING_TYPE_CHOICES = [
        ('Rented apartment', 'Rented apartment'),
        ('House / apartment', 'House / apartment'),
        ('Municipal apartment', 'Municipal apartment'),
        ('With parents', 'With parents'),
        ('Co-op apartment', 'Co-op apartment'),
        ('Office apartment', 'Office apartment'),
    ]
    
    # Occupation type choices
    OCCUPATION_TYPE_CHOICES = [
        ('Laborers', 'Laborers'),
        ('Core staff', 'Core staff'),
        ('Sales staff', 'Sales staff'),
        ('Managers', 'Managers'),
        ('Drivers', 'Drivers'),
        ('High skill tech staff', 'High skill tech staff'),
        ('Accountants', 'Accountants'),
        ('Medicine staff', 'Medicine staff'),
    ]

    owns_car = models.CharField(max_length=1, choices=CAR_OWNERSHIP_CHOICES)
    owns_property = models.CharField(max_length=1, choices=REALTY_OWNERSHIP_CHOICES)
    num_children = models.IntegerField()
    total_income = models.FloatField()
    education_type = models.CharField(max_length=100, choices=EDUCATION_TYPE_CHOICES)
    family_status = models.CharField(max_length=100, choices=FAMILY_STATUS_CHOICES)
    housing_type = models.CharField(max_length=100, choices=HOUSING_TYPE_CHOICES)
    age = models.IntegerField()
    employment_duration = models.IntegerField()
    occupation_type = models.CharField(max_length=100, choices=OCCUPATION_TYPE_CHOICES)
    number_of_family_members = models.IntegerField()
    prediction_result = models.IntegerField(null=True)
