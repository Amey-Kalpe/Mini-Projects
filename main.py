"""Workout Tracker
"""

import base64
from datetime import datetime
import requests

APP_ID = "MzZlYjgzMDU="
API_KEY = "MDk1NTFjMmYxNjIzYjQ3ODVkOWVjZGY0OTVmNDBiN2E="
EXERCISE_URL = "https://trackapi.nutritionix.com/v2/natural/exercise"
ADD_ROW_SHEETY_URL = "aHR0cHM6Ly9hcGkuc2hlZXR5LmNvLzEwMjBiMWZmZGJjNjAzMmVjNDdiYTZkZDVjM2JlYjNhL3dvcmtvdXRUcmFja2VyL3dvcmtvdXRz"
BEARER_AUTH_TOKEN = "QmVhcmVyIGFzZGpraGFzZGtuYmFzZGp5Z2V3cmZhc2RmLS0="

query = input("Tell me which exercises you did: ")

params = {
    "query": f"{query}",
    "gender": "male",
    "weight_kg": 52.4,
    "height_cm": 167.64,
    "age": 22,
}

headers = {"x-app-id": base64.b64decode(APP_ID), "x-app-key": base64.b64decode(API_KEY)}

response = requests.post(EXERCISE_URL, json=params, headers=headers)
resp_json = response.json()

print("Processes exercises successfully.")

for exercise in resp_json.get("exercises"):
    exercise_name = exercise.get("name")
    duration = exercise.get("duration_min")
    calories = exercise.get("nf_calories")

    sheety_headers = {
        "Content-Type": "application/json",
        "Authorization": base64.b64decode(BEARER_AUTH_TOKEN),
    }

    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    time = now.strftime("%H:%M:%S")

    sheety_add_row_params = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise_name.title(),
            "duration": duration,
            "calories": calories,
        }
    }

    sheety_response = requests.post(
        base64.b64decode(ADD_ROW_SHEETY_URL),
        json=sheety_add_row_params,
        headers=sheety_headers,
    )
    print(sheety_response.text)
