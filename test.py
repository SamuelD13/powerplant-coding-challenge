import requests
import json
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Test the /productionplan API endpoint")
    parser.add_argument('filename', type=str, help="The JSON file containing the data to send")
    args = parser.parse_args()

    url = "http://127.0.0.1:8888/productionplan"

    with open(args.filename, 'r') as file:
        payload = json.load(file)

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print(f"Failed with status code {response.status_code}: {response.json()}")

if __name__ == '__main__':
    main()