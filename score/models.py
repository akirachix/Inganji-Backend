from time import timezone
from django.db import models
from django.utils import timezone

from django.db import models
from django.forms import ValidationError
from farmers.models import FarmersManagement


class Score(models.Model):
    credit_score_id = models.AutoField(primary_key=True)
    farmer_id = models.ForeignKey(FarmersManagement, on_delete=models.CASCADE)
    score = models.SmallIntegerField()
    credit_worthiness = models.CharField(max_length=20)
    loan_range = models.CharField(max_length=50)
    last_checked_date = models.DateField()
    is_eligible = models.BooleanField(default=False)

    def clean(self):
        if not (0 <= self.score <= 850):
            raise ValidationError("Score must be between 0 and 850.")
        if self.last_checked_date > timezone.now().date():
            raise ValidationError("Last checked date cannot be in the future.")

    def __str__(self):
        return f"Score for {self.farmer_id}: {self.credit_score_id}"


