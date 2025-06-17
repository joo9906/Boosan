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

class Pill(models.Model):
    PILL_TYPE_CHOICES = [
        ('TAB', '정제'),
        ('CAP', '캡슐'),
        ('SYR', '시럽'),
        ('INJ', '주사제'),
        ('POW', '가루약'),
        ('GEL', '겔제'),
        ('OTR', '기타'),
    ]

    name = models.CharField(max_length=100, verbose_name='약 이름')
    type = models.CharField(max_length=3, choices=PILL_TYPE_CHOICES, verbose_name='약 종류')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='입력일')
    image = models.ImageField(upload_to='pill_images/', blank=True, null=True, verbose_name='약봉투 사진')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pills', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
