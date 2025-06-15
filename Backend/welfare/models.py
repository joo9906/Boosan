from django.db import models

# Create your models here.
class DongbaekFranchise(models.Model):
    name = models.CharField(max_length=20)
    roadNum = models.TextField()
    lat = models.FloatField()
    lon = models.FloatField()
    
class WelfareCenter(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    tel = models.CharField(max_length=20)
    type = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
