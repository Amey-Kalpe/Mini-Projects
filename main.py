"Pixela Habit Tracker"

from datetime import datetime
import requests

PIXELA_URL = "https://pixe.la/v1/users"
USERNAME = "ameykalpe"
ACCESS_TOKEN = "abchsdety12345##"
GRAPH_ID = "graph1"

headers = {"X-USER-TOKEN": ACCESS_TOKEN}


# pixela_create_user_url = PIXELA_URL
# params = {
#     "token": "abchsdety12345##",
#     "username": "ameykalpe",
#     "agreeTermsOfService": "yes",
#     "notMinor": "yes",
# }

# response = requests.post(pixela_create_user_url, json=params)

# pixela_create_graph_url = f"{PIXELA_URL}/{USERNAME}/graphs"
# params = {
#     "id": "graph1",
#     "name": "Calory Counter Graph",
#     "unit": "calory",
#     "type": "int",
#     "color": "momiji",
# }

now = datetime.now()
today = now.strftime("%Y%m%d")

pixela_update_graph_url = f"{PIXELA_URL}/{USERNAME}/graphs/{GRAPH_ID}"
params = {
    "date": today,
    "quantity": "2400",
}

response = requests.post(pixela_update_graph_url, json=params, headers=headers)

# pixela_update_pixel_url = f"{PIXELA_URL}/{USERNAME}/graphs/{GRAPH_ID}/{today}"

# pixela_delete_pixel_endpoint = f"{PIXELA_URL}/{USERNAME}/graphs/{GRAPH_ID}/{today}"

# response = requests.delete(pixela_delete_pixel_endpoint, headers=headers)

print(response.text)
