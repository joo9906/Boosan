from django.db import models
from account.models import User

class MedicalFacility(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50) 
    address = models.TextField()
    tel = models.CharField(max_length=15)
    latitude = models.FloatField()
    longitude = models.FloatField()
    bus_stop = models.CharField(max_length=20, default='정보 없음')
    holiday_open = models.BooleanField(default=False)
    is_partnered = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class FacilityVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='facility_visits')
    facility = models.ForeignKey(MedicalFacility, on_delete=models.CASCADE, related_name='visits')
    visit_time = models.DateTimeField()
    service_used = models.TextField()
