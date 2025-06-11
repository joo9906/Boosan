from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    card_num = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)
    support_type = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    tel = models.CharField(max_length=20)

    class Meta:
        db_table = 'user'
