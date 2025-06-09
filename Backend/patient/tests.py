from django.test import TestCase
import requests
import xml.etree.ElementTree as ET

url = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEmrrmRltmUsefulSckbdInfoInqire'
params ={'serviceKey' : 'YPMIUwyLBekZB59rz0n/i1isnn64h00ZistxhbPHOy5kwoWiFZXqXxoU+vntsSRZXnwHLrLBlILjFE/rbpQlXQ==', 'STAGE1' : '부산광역시', 'STAGE2' : '서구', 'pageNo' : '1', 'numOfRows' : '10' }

response = requests.get(url, params=params)
parsing = ET.fromstring(response.content)
print('파싱', parsing)

for item in parsing.iter("item"):
    name = item.find("dutyName").text        # 병원 이름
    tel = item.find("dutyTel3").text         # 병원 전화번호
    icu = item.find("hvcc")                  # 중환자실 병상 수 (없을 수도 있음)
    erbed = item.find('hvec').text
    icu_text = icu.text if icu is not None else "정보 없음"
    if name =='동아대학교병원':
        print(f'병원 이름 : {name}, 응급실 병상 수: {erbed}')


