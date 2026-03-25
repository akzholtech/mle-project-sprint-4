
import requests
from dotenv import load_dotenv

load_dotenv()

type = "offline"

user_sample_id = 1155725
item_sample_id = 51320248

recommendations_url = "http://127.0.0.1:8000"

if type == "offline":

    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    params = {"user_id": user_sample_id, "k": 5}

    resp = requests.post(f"{recommendations_url}/recommendations", headers=headers, params=params)

    if resp.status_code == 200:
        recs = resp.json()
    else:
        recs = []
        print(f"status code: {resp.status_code}")

    print(recs)

else:

    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    params = {"item_id": item_sample_id, "k": 5}

    resp = requests.post(f"{recommendations_url}/similar_items", headers=headers, params=params)

    if resp.status_code == 200:
        recs = resp.json()
    else:
        recs = []
        print(f"status code: {resp.status_code}")

    print(recs)
