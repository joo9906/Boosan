from rest_framework import serializers
from .models import MedicalFacility

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalFacility
        fields = ['id', 'name', 'address', 'tel', 'type', 'latitude', 'longitude'] 