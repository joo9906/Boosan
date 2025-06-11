from django.db import models
from account.models import User

# Create your models here.

class PublicSupport(models.Model):
    support_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supports')
    title = models.CharField(max_length=200)
    description = models.TextField()
    eligibility = models.TextField()
    apply_url = models.TextField()
    support_type = models.CharField(max_length=20)  # welfare 또는 culture

    class Meta:
        db_table = 'public_support'

class WelfareSupportDetail(models.Model):
    support = models.OneToOneField(PublicSupport, on_delete=models.CASCADE, primary_key=True)
    deadline = models.DateField()

    class Meta:
        db_table = 'welfare_support_detail'

class CultureSupportDetail(models.Model):
    support = models.OneToOneField(PublicSupport, on_delete=models.CASCADE, primary_key=True)
    category = models.CharField(max_length=50)
    location = models.TextField()

    class Meta:
        db_table = 'culture_support_detail'

class UserSupportMatch(models.Model):
    match_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_matches')
    support = models.ForeignKey(PublicSupport, on_delete=models.CASCADE)
    is_notified = models.BooleanField(default=False)
    matched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_support_match'

class CounselRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='counsel_requests')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    emergency = models.BooleanField(default=False)

    class Meta:
        db_table = 'counsel_request'
