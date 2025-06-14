from django.db import models

# Create your models here.
class dongbaekFranchise(models.Model):
    name = models.CharField(max_length=20)
    roadNum = models.TextField()
    lat = models.FloatField()
    lon = models.FloatField()
    
    