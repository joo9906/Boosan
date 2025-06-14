import json

# 동백화폐 가맹점 현황 데이터 사용 URL: https://data.busan.go.kr/bdip/opendata/detail.do?publicdatapk=15088786&searchKeyword=%EB%8F%99%EB%B0%B1&searchOption=AND&uuid=b0dbf7bc-4cd4-4f9c-a01f-27c9515e1d13
# 파일 경로 설정
input_path = "G:/싸피/코드 관련/Boosan/Backend/welfare/fixtures/dongbaek.json"
output_path = "G:/싸피/코드 관련/Boosan/Backend/welfare/fixtures/dongbaek_fixture.json"
model_name = "welfare.dongbaekFranchise"

# 중괄호 개수로 객체 단위 분리
raw_objects = []
buffer = ""
brace_count = 0

with open(input_path, "r", encoding="utf-8") as infile:
    content = infile.read()
    for char in content:
        buffer += char
        if char == "{":
            brace_count += 1
        elif char == "}":
            brace_count -= 1
        if brace_count == 0 and buffer.strip():
            try:
                obj = json.loads(buffer)
                raw_objects.append(obj)
                buffer = ""
            except json.JSONDecodeError:
                continue

# list 객체 안에 또 list가 있는 경우 flatten
flattened_objects = []
for obj in raw_objects:
    if isinstance(obj, list):
        flattened_objects.extend(obj)
    elif isinstance(obj, dict):
        flattened_objects.append(obj)

#  Django fixture 형태로 변환
fixtures = []
for idx, item in enumerate(flattened_objects, start=1):
    fixture = {
        "model": model_name,
        "pk": idx,
        "fields": {
            "name": item.get("frcsNm", "")[:20],
            "roadNum": item.get("roadNm", ""),
            "lat": float(item.get("lat", 0)),
            "lon": float(item.get("lot", 0)),
        }
    }
    fixtures.append(fixture)

# JSON 파일로 저장
with open(output_path, "w", encoding="utf-8") as outfile:
    json.dump(fixtures, outfile, indent=2, ensure_ascii=False)