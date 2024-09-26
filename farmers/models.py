from django.db import models
from django.db.models import Max, F, Value
from django.db.models.functions import Cast, Replace
from django.utils import timezone
from django.db import transaction
from django.core.validators import RegexValidator
from cooperative.models import Cooperative


class FarmersManagement(models.Model):
    farmer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\d+$', 'Phone number must be numeric')]
    )
    created_at = models.DateField(auto_now_add=True)
    cooperative_number = models.CharField(max_length=20, unique=True, blank=True, null=True, editable=False)
    sacco_name = models.CharField(max_length=20)
    cooperative_id = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    def generate_cooperative_number(self):
        current_year = timezone.now().year
        prefix = "C"
        with transaction.atomic():
            last_number = FarmersManagement.objects.filter(
                cooperative_number__startswith=f"{prefix}/{current_year}/"
            ).annotate(
                numeric_part=Cast(Replace(F('cooperative_number'), Value(f"{prefix}/{current_year}/"), Value('')), IntegerField())
            ).aggregate(Max('numeric_part'))['numeric_part__max']
            if last_number is None:
                return f"{prefix}/{current_year}/1"
            new_number = last_number + 1
            return f"{prefix}/{current_year}/{new_number}"
    def save(self, *args, **kwargs):
        if not self.cooperative_number:
            self.cooperative_number = self.generate_cooperative_number()
        with transaction.atomic():
            super().save(*args, **kwargs)