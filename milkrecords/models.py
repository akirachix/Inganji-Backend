from django.db import models
from django.utils import timezone
from farmers.models import FarmersManagement
from django.core.exceptions import ValidationError


class MilkRecords(models.Model):
    record_id = models.AutoField(primary_key=True)
    farmer_id = models.ForeignKey(FarmersManagement, on_delete=models.CASCADE, related_name='milk_records')
    milk_quantity = models.IntegerField()  
    price = models.IntegerField(default=70)
    date = models.DateField()

    def clean(self):
        if self.milk_quantity is not None and self.milk_quantity < 0:
            raise ValidationError('Milk quantity cannot be negative.')
        if self.price is not None and self.price < 0:
            raise ValidationError('Price cannot be negative.')
        if self.date is None:
            raise ValidationError('Date cannot be empty.')
        if self.date > timezone.now().date():
            raise ValidationError('Date cannot be in the future.')
        

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Milk record for {self.farmer_id} on {self.date}"

    