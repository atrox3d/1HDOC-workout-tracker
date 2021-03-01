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


def ASCII_ROW(char="-", width=80):
    print(char * width)


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
    # if query from input is None use default in dict
    if query:
        params["query"] = query

    ASCII_ROW("#")
    # print("nutritionix query: ", json.dumps(params, indent=4))
    print("nutritionix payload      : ", params)
    ASCII_ROW("#")

    response = requests.post(url=NUTRITIONIX_ENDPOINT, json=params, headers=headers)

    print("nutritionix status code  : ", response.status_code)
    ASCII_ROW()
    print("NUTRINIONIX RESPONSE")
    ASCII_ROW()
    print("nutritionix response data: ", json.dumps(response.json(), indent=4))

    return response


def update_sheety(exercise: dict) -> requests.models.Response:
    update_sheety.SECONDS_IN_A_DAY = 24 * 60 * 60
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
    now_time = td.seconds / update_sheety.SECONDS_IN_A_DAY

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
    ASCII_ROW("#")
    print("google payload: ", payload)
    ASCII_ROW("#")
    response = requests.post(SHEETY_ENDPOINT, json=payload)

    print("google status code       : ", response.status_code)
    print("-" * 80)
    print("GOOGLE RESPONSE")
    print("-" * 80)
    print("google response text     : ", response.text)

    return response


################################################################################
while True:
    query = input("\n\n\n\nTell me wich exercises you did: ")

    nutritionix_response = query_nutritionix(query)
    nutritionix_data = nutritionix_response.json()

    for currrent_exercise in nutritionix_data["exercises"]:
        sheety_response = update_sheety(currrent_exercise)

    print("*" * 80)
    print(f"last query: '{query}'")
    print("*" * 80)
