import myob
import requests
import json
import datetime as dt

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
        "gender": "female",
        "weight_kg": 50,
        "height_cm": 154.0,
        "age": 38
    }
    if query:
        params["query"] = query

    print("query: ", json.dumps(params, indent=4))
    print("#" * 80)

    response = requests.post(url=NUTRITIONIX_ENDPOINT, json=params, headers=headers)
    print(response.status_code)
    # print(type(response))
    # data = response.json()
    # print(type(data))
    # print(json.dumps(data, indent=4))
    return response


def update_sheety(exercise: dict) -> requests.models.Response:
    time_iso = dt.datetime.now().time()
    #
    #   too convoluted
    #   https://gist.github.com/angelabauer/164864b78175bb1ecd3d3fd7f4ee39b7#gistcomment-3596417
    #
    now_time = ((time_iso.hour + ((time_iso.minute + (time_iso.second / 60.0)) / 60.0)) / 24.0)
    #
    # or simpler
    # https://stackoverflow.com/a/39536110
    # https://stackoverflow.com/a/9574948
    # https://stackoverflow.com/a/42230265
    # https://developers.google.com/sheets/api/guides/concepts#datetime_serial_numbers
    #
    now_time = time_iso.hour / 24.0 + \
               time_iso.minute / 60.0 + \
               time_iso.second / 60.0
    #
    # or BETTER
    # https://stackoverflow.com/a/19813554
    #
    td = dt.timedelta(
        hours=time_iso.hour,
        minutes=time_iso.minute,
        seconds=time_iso.second,
        microseconds=time_iso.microsecond
    )
    SECONDS_IN_A_DAY = 24 * 60 * 60
    now_time = td.seconds / SECONDS_IN_A_DAY

    payload = {
        "workout": {
            "date": dt.datetime.strftime(dt.datetime.now(), "%Y%m%d"),
            # "time": dt.strftime(dt.now(), "%H:%M:%S %p"),
            # "time": dt.strftime(dt.now(), "%X"),
            "time": now_time,
            "exercise": exercise["name"],
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
    print("payload: ", payload)
    response = requests.post(SHEETY_ENDPOINT, json=payload)
    return response


################################################################################
while True:
    query = input("\n\n\n\nciao, cosa hai fatto: ")

    nutritionix_response = query_nutritionix(query)
    nutritionix_data = nutritionix_response.json()
    print("-" * 80)
    print("RISPOSTA NUTRITIONIX")
    print("-" * 80)
    print(json.dumps(nutritionix_data, indent=4))
    print("#" * 80)

    for exercise in nutritionix_data["exercises"]:
        sheety_response = update_sheety(exercise)
        print("-" * 80)
        print("RISPOSTA GOOGLE")
        print("-" * 80)
        print("status code: ", sheety_response.status_code)
        print("response text: ", sheety_response.text)

    print("*" * 80)
    print(query)
    print("*" * 80)

