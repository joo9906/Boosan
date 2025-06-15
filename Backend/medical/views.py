from django.http import JsonResponse
from .models import MedicalFacility

def hospital_list(request):
    hospitals = MedicalFacility.objects.all()
    data = [{
        'id': hospital.id,
        'name': hospital.name,
        'address': hospital.address,
        'tel': hospital.tel,
        'type': hospital.type,
        'latitude': hospital.latitude,
        'longitude': hospital.longitude
    } for hospital in hospitals]
    return JsonResponse(data, safe=False)
