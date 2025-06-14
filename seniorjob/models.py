from django.db import models
from account.models import User

class SeniorJob(models.Model):
    gugun = models.CharField(max_length=30)
    perform_inst = models.CharField(max_length=100)
    bsns_nm = models.CharField(max_length=100)
    bsns_kind = models.CharField(max_length=50)
    tel = models.CharField(max_length=20)
    people = models.IntegerField()
    bsns_main_activ = models.TextField()
    bsns_sdate = models.DateField()
    bsns_fdate = models.DateField()
    data_day = models.DateField()
    record_year = models.IntegerField()

    def __str__(self):
        return f"{self.bsns_nm} ({self.gugun})"

class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    job = models.ForeignKey(SeniorJob, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username}'s application for {self.job.bsns_nm}" 