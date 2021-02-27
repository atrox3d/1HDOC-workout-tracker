import myob
import requests
import json
from datetime import datetime as dt

NUTRITIONIX_APPID = myob.NUTRITIONIX_APPID
NUTRITIONIX_APPKEY = myob.NUTRITIONIX_APPKEY
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

SHEETY_USER = myob.SHEETY_USER
SHEETY_PROJECT = myob.SHEETY_PROJECT
SHEETY_SHEET = myob.SHEETY_SHEET
SHEETY_ENDPOINT = f"https://api.sheety.co/{SHEETY_USER}/{SHEETY_PROJECT}/{SHEETY_SHEET}"


def query_nutritionix(query: str = None) -> requests.models.Response:
    headers = {
        "x-app-id": NUTRITIONIX_APPID,
        "x-app-key": NUTRITIONIX_APPKEY
    }

    params = {
        # "query": "ran 3 miles",
        "query": "swam 40 min and ran 3km and 30 min pushups",
        "gender": "male",
        "weight_kg": 98,
        "height_cm": 170.0,
        "age": 50
    }
    if query:
        params["query"] = query

    response = requests.post(url=NUTRITIONIX_ENDPOINT, json=params, headers=headers)
    print(response.status_code)
    # print(type(response))
    # data = response.json()
    # print(type(data))
    # print(json.dumps(data, indent=4))
    return response


def update_sheety(exercise: dict) -> requests.models.Response:
    # print(json.dumps(exercise, indent=4))
    payload = {
        "workout": {
            "date": dt.strftime(dt.now(), "%Y%m%d"),
            "time": dt.strftime(dt.now(), "%H:%M:%S %p"),
            "exercise": exercise["name"],
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
    print(payload)
    response = requests.post(SHEETY_ENDPOINT, json=payload)
    return response


################################################################################
nutritionix_response = query_nutritionix()
nutritionix_data = nutritionix_response.json()

for exercise in nutritionix_data["exercises"]:
    response = update_sheety(exercise)
    print(response.status_code)
    print(response.text)
