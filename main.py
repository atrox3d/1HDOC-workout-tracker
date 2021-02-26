import myob
import requests
import json

APP_ID = myob.APP_ID
APP_KEY = myob.APP_KEY
ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

HEADERS = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY
}

params = {
    # "query": "ran 3 miles",
    "query": "swam 40 min and ran 3km and 30 min pushups",
    "gender": "male",
    "weight_kg": 98,
    "height_cm": 170.0,
    "age": 50
}

# query = input("Tell me which exercises you did: ")

# params["query"] = query

response = requests.post(url=ENDPOINT, json=params, headers=HEADERS)
print(response.status_code)
print(
    json.dumps(response.json(), indent=4)
)
