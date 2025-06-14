from urllib.parse import urlencode
import requests

base_url = 'http://apis.data.go.kr/6260000/MedicInstitService/MedicalInstitInfo'
query = {
    'serviceKey': 'awCBBa0nJ2QEK14SeWUgrBWeleAl%2BmSwrlBhurGvNOthTe7pBbIJwU%2FtuFmQbDZyIgdr2K7%2B%2FJdCYN4k%2B50B5A%3D%3D',
    'pageNo': '1',
    'numOfRows': '10',
    'instit_nm' : '' , 
    'instit_kind' : '',
}

response = requests.get(base_url, params=query, verify=False)
print('현제 정보', response.text)
