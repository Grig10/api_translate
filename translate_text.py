from requests.structures import CaseInsensitiveDict
import webbrowser
import subprocess
import requests
import json
import os
import time



def extract_id_from_data(data):
    dictData = json.loads(json.dumps(data))
    print(dictData["id"])
    return dictData["id"]

def extract_streaming_from_data(data):
    dicData = json.loads(json.dumps(data))
    print(dicData)
    print(dicData["streaming_url"])
    return dicData["streaming_url"]

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
   streaming = extract_streaming_from_data(resp.json())
   resp.close()
else:
    print("Received unexpected status code {}".format(resp.status_code))

current_dir = os.getcwd() + "/Desktop"
path_translate_text = os.path.join(current_dir, 'translate_text.txt')
path_result_text = os.path.join(current_dir, 'result.txt')
with open(path_translate_text, 'r', encoding='cp1251', errors='ignore') as f:
    data = f.read()

result = request_to_translate_text(id, data.strip())

webbrowser.get('firefox').open(streaming)

proc = subprocess.Popen(["""ffmpeg -f avfoundation -i "1:0" -vf "crop=2500:1400:500:500" -pix_fmt yuv420p -y -r 10 out1.mp4"""], shell=True)

time.sleep(15)

proc.terminate()

















