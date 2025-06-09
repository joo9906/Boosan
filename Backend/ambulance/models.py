from django.db import models
from django.contrib.gis.db import models as gis_models
from hospital.models import Hospital
from patient.models import Patient

class Ambulance(models.Model):
    ambulance_id = models.AutoField(primary_key=True, verbose_name='구급차 고유 ID')
    gps_location = gis_models.PointField(verbose_name='환자 위치 정보')
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='이송 병원 ID')
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='이송 환자')
    status = models.CharField(max_length=50, verbose_name='대기, 이송 중, 도착 등')
    medic_id = models.CharField(max_length=50, verbose_name='구급대원 사번')
    medic_name = models.CharField(max_length=50, verbose_name='구급대원 이름')

    def __str__(self):
        return f"{self.ambulance_id} - {self.status}"
