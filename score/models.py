from django.db import models

from django.db import models
from farmers.models import FarmersManagement

# Create your models here.

class Score(models.Model):
    credit_score_id = models.AutoField(primary_key=True)
    farmer = models.ForeignKey('farmers.FarmersManagement', on_delete=models.CASCADE)
    score = models.SmallIntegerField()
    credit_worthiness = models.CharField(max_length = 20)
    loan_range = models.CharField(max_length = 50)
    last_checked_date =models.DateField()
    status = models.CharField(max_length = 50)


    def __str__(self):
        return f"Score for {self.farmer}: {self.credit_score}"

