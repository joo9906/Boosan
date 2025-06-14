from django.db import models
from boosanbackend.account.models import User

class MedicalFacility(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)  # hospital, pharmacy, welfare
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_partnered = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class FacilityVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='facility_visits')
    facility = models.ForeignKey(MedicalFacility, on_delete=models.CASCADE, related_name='visits')
    visit_time = models.DateTimeField()
    service_used = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s visit to {self.facility.name} at {self.visit_time}" 