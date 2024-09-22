from django.db import models
from users.models import UserProfile
class Cooperative(models.Model):
    cooperative_id = models.AutoField(primary_key=True)
    cooperative_name = models.CharField(max_length=255)  
    user = models.ForeignKey(UserProfile ,on_delete=models.CASCADE)

    def __str__(self):
        return self.cooperative_name