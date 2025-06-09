from django.db import models
from django.contrib.gis.db import models as gis_models

class Hospital(models.Model):
    hospital_id = models.AutoField(primary_key=True, verbose_name='병원 고유 ID')
    name = models.CharField(max_length=100, verbose_name='병원명')
    location = gis_models.PointField(verbose_name='병원 위치')
    capacity = models.IntegerField(verbose_name='수용 가능 인원')
    equipment = models.TextField(verbose_name='장비 보유 정보')

    def __str__(self):
        return self.name
