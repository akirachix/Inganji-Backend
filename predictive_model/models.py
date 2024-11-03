from django.db import models

class Prediction(models.Model):
   
    CAR_OWNERSHIP_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No')
    ]
    
    REALTY_OWNERSHIP_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No')
    ]
    
    EDUCATION_TYPE_CHOICES = [
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
        ('Higher', 'Higher'),
        ('Postgraduate', 'Postgraduate'),
    ]
    
    FAMILY_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
        ('Separated', 'Separated'),
    ]
    
    HOUSING_TYPE_CHOICES = [
        ('Rent', 'Rent'),
        ('Own', 'Own'),
        ('Mortgage', 'Mortgage'),
        ('Other', 'Other'),
    ]

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
