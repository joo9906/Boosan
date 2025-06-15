import json

with open('welfare_center.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for obj in data:
    tel = obj['fields'].get('tel')
    if isinstance(tel, int) and str(tel).startswith('51'):
        obj['fields']['tel'] = '0' + str(tel)

with open('welfare_center.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2) 