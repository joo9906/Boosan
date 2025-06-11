from django.db import models
from account.models import User

# Create your models here.

class Guardian(models.Model):
    guardian_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)

    class Meta:
        db_table = 'guardian'

class UserGuardian(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guardians')
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=50)

    class Meta:
        db_table = 'user_guardian'
