from django.db import models
from users.models import UserProfile

class Sacco(models.Model):
    sacco_id = models.AutoField(primary_key=True)
    sacco_name = models.CharField(max_length=255)  
    user = models.ForeignKey(UserProfile ,on_delete=models.CASCADE)


    def __str__(self):
        return self.sacco_name