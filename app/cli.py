import requests
import json

url_local = 'http://127.0.0.1:8080/send'
url_remote = 'default.bigqueue.melicloud.com:8080'

url = url_local

payload = {'points': 1000}

r = requests.get(url, data=json.dumps(payload))
print(r.json())

