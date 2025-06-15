from urllib.parse import urlencode
import requests, json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("decoding_API_KEY")

url = 'http://apis.data.go.kr/6260000/MedicInstitService/MedicalInstitInfo'
params ={'serviceKey' : API_KEY , 'pageNo' : '1' , 'numOfRows' : '1000' , 'resultType': 'json', 'instit_nm': ''}

# response = requests.get(url, params=params)
response = requests.get(url, params=params, verify=False)
data = response.json()
items = data['response']['body']['items']['item']

fixture = []

idx = 1
for item in items:
    hos_name = item['instit_nm']
    hos_kind = item['instit_kind']
    address = item['street_nm_addr']
    tel = item['tel']
    bus_stop = item['organ_loc']
    lat = item['lat']
    lon = item['lng']
    holiday_open = False
    if item['saturday']:
        holiday_open = True

    fixture.append({
        "model": "medical.medicalfacility",
        "pk": idx,
        "fields": {
            "name": hos_name,
            "type": hos_kind,
            "address": address,
            "tel": tel,
            "latitude": lat,
            "longitude": lon,
            "bus_stop": bus_stop,
            "holiday_open": holiday_open,
            "is_partnered": False,
        }
    })
    idx += 1

with open('hospital_info.json', 'w', encoding='utf-8') as f:
    json.dump(fixture, f, ensure_ascii=False, indent=2)