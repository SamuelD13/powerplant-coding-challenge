import requests
import json

if __name__ == '__main__':

    url = "http://127.0.0.1:8888/productionplan"

    with open('example_payloads/payload2.json', 'r') as file:
        payload = json.load(file)

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print(f"Failed with status code {response.status_code}: {response.json()}")