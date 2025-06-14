from django.db import models
from account.models import User
from medical.models import FacilityVisit, MedicalFacility

class HealthRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_records')
    record_date = models.DateTimeField()
    blood_pressure = models.CharField(max_length=50)
    blood_sugar = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    notes = models.TextField()
    health_condition = models.CharField(max_length=100)
    facility_visit = models.ForeignKey(FacilityVisit, on_delete=models.SET_NULL, null=True, blank=True, related_name='health_records')

    def __str__(self):
        return f"{self.user.username}'s health record on {self.record_date}"

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    type = models.CharField(max_length=50)
    content = models.TextField()
    remind_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    facility = models.ForeignKey(MedicalFacility, on_delete=models.SET_NULL, null=True, blank=True, related_name='reminders')
    health_record = models.ForeignKey('HealthRecord', on_delete=models.SET_NULL, null=True, blank=True, related_name='reminders')

    def __str__(self):
        return f"{self.user.username}'s {self.type} reminder at {self.remind_at}"

class NotificationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    reminder = models.ForeignKey(Reminder, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')

    def __str__(self):
        return f"Notification for {self.user.username} at {self.sent_at}" 