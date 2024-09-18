from django.db import models
from django.db.models import Max



class FarmersManagement(models.Model):
    farmer_id = models.AutoField(primary_key=True) 
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=15)
    created_at=models.DateField(auto_now_add=True)
    cooperative_number = models.PositiveIntegerField(unique=True, blank=True, null=True, editable=False)
    sacco_name= models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def generate_cooperative_number(self):
        last_number = FarmersManagement.objects.aggregate(Max('cooperative_number'))['cooperative_number__max']
        if last_number is None:
            return 1
        return last_number + 1

    def save(self, *args, **kwargs):
        if self.cooperative_number is None:
            self.cooperative_number = self.generate_cooperative_number()
        super().save(*args, **kwargs)
    
  
    