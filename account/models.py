from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    is_guardian = models.BooleanField(default=False)
    guardian_for = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='guardians')

    def __str__(self):
        return self.username

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='detail')
    income_level = models.ForeignKey('WelfareEligibility', on_delete=models.SET_NULL, null=True)
    mobility = models.CharField(max_length=100)
    digital_literacy = models.CharField(max_length=100)
    communication_style = models.CharField(max_length=100)
    living_situation = models.CharField(max_length=100)
    religion = models.CharField(max_length=100)
    preferred_activity_time = models.CharField(max_length=100)
    social_preference = models.CharField(max_length=100)
    hobby = models.TextField()
    disposition = models.TextField()
    personality = models.TextField()
    age_group = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username}'s details"

class WelfareEligibility(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='welfare_eligibility')
    is_low_income = models.BooleanField(default=False)
    is_disable = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s welfare eligibility" 