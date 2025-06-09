from django.db import models
from django.contrib.gis.db import models as gis_models

class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True, verbose_name='환자 고유 ID')
    age = models.IntegerField(verbose_name='나이')
    gender = models.CharField(max_length=10, verbose_name='성별')
    condition = models.CharField(max_length=10, verbose_name='중증도: 상/중/하')
    created_at = models.DateTimeField(verbose_name='접수 시각')
    patient_location = gis_models.PointField(verbose_name='환자 주소')

    def __str__(self):
        return f"{self.patient_id} - {self.age}세"

class Patient_data(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='기록 고유 ID')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    heart_rate = models.IntegerField(verbose_name='심박수')
    systolic_bp = models.IntegerField(verbose_name='최고 혈압')
    diastolic_bp = models.IntegerField(verbose_name='최저 혈압')
    pain_area = models.CharField(max_length=100, verbose_name='통증 부위')
    pain_level = models.IntegerField(verbose_name='통증 정도 (0~10)')
    respiratory_rate = models.IntegerField(verbose_name='호흡수')
    temperature = models.FloatField(verbose_name='체온')
    spo2 = models.FloatField(verbose_name='산소포화도')
    consciousness = models.CharField(max_length=50, verbose_name='의식 수준')
    created_at = models.DateTimeField(verbose_name='측정 시각')

    def __str__(self):
        return f"{self.patient.patient_id} - {self.created_at}"
