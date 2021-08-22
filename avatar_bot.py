import requests
import json
import os
from requests.structures import CaseInsensitiveDict

def extract_id_from_data(data):
    dictData = json.loads(json.dumps(data))
    return dictData["id"]

def request_to_translate_text(id, text):
    url = "http://84.201.181.102:8090/api/v1/avatar/" + id + "/translate/text/"
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    data = {"text": text, "speed": 1}
    resp = requests.post(url, headers=headers, json=data)  
    result = resp.json()
    resp.close()
    return result
    

url = "http://84.201.181.102:8090/api/v1/avatar/take/"

headers = CaseInsensitiveDict()

headers["accept"] = "application/json"

resp = requests.get(url, headers=headers)
 
if resp.status_code == 200:
   id = extract_id_from_data(resp.json())
   resp.close()
else:
    print(resp.raise_for_status())

current_dir = os.getcwd() + "/Desktop"
path_translate_text = os.path.join(current_dir, 'translate_text.txt')
path_result_text = os.path.join(current_dir, 'result.txt')
with open(path_translate_text, 'r', encoding='cp1251', errors='ignore') as f:
    data = f.read()

result = request_to_translate_text(id, data.strip())

with open(path_result_text, 'w', encoding='cp1251', errors='ignore') as f:
    json.dump(result, f, ensure_ascii=False)




