import requests
import json
import os

api_key = "8efd6a55d157ee2cdaee567709846929faaa8e2620f67f7abf6e34c1db260649"
base_url = "https://otx.alienvault.com"
endpoint = "/api/v1/pulses/subscribed"
headers = {
    "X-OTX-API-KEY": api_key
}
params = {
    "limit": 500000
}
response = requests.get(base_url + endpoint, headers=headers, params=params)
if response.status_code == 200:
    data = response.json()
    pulses = data["results"]
    pulses_json = json.dumps(pulses, default=str)
    if not os.path.exists('json_files'):
        os.mkdir('json_files')
    with open("json_files/data.json", "w")as outfile:
        outfile.write(pulses_json)
