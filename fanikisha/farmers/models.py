from django.utils import timezone
from django.db import models
from django.db.models import Max
# from cooperative.models import Cooperative


class FarmersManagement(models.Model):
    farmer_id = models.AutoField(primary_key=True) 
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=15)
    created_at=models.DateField(auto_now_add=True)
    cooperative_number = models.CharField(max_length=20, unique=True, blank=True, null=True, editable=False)
    sacco_name = models.CharField(max_length=20)
    """ This code is to show the relationship between the cooperative and the farmers model"""
    # cooperative_name = models.ForeignKey(Cooperative, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.cooperative.name}"

    def generate_cooperative_number(self):
        current_year = timezone.now().year
        # Use the first letter of the cooperative's name as the prefix
        prefix = self.cooperative_name.name[0].upper()  
        
        last_number = FarmersManagement.objects.filter(
            cooperative_number__startswith=f"{prefix}/{current_year}/"
        ).aggregate(Max('cooperative_number'))['cooperative_number__max']
        
        if last_number is None:
            return f"{prefix}/{current_year}/1"
        
        # Extract the last number and increment
        last_num = int(last_number.split('/')[-1])
        new_number = last_num + 1
        
        return f"{prefix}/{current_year}/{new_number}"

    def save(self, *args, **kwargs):
        if self.cooperative_number is None:
            self.cooperative_number = self.generate_cooperative_number()
        super().save(*args, **kwargs)

    
  
    