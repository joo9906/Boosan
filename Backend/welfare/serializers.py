from rest_framework import serializers
from .models import WelfareCenter

class WelfareCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WelfareCenter
        fields = ['id', 'name', 'address', 'tel', 'type', 'latitude', 'longitude'] 