from django.http import JsonResponse
from .models import WelfareCenter

def welfare_center_list(request):
    centers = WelfareCenter.objects.all()
    data = [{
        'id': center.id,
        'name': center.name,
        'address': center.address,
        'tel': center.tel,
        'type': center.type,
        'latitude': center.latitude,
        'longitude': center.longitude
    } for center in centers]
    return JsonResponse(data, safe=False)
