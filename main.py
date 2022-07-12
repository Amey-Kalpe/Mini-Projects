"""Get the best deal for flight booking notified based on the To and From location in google sheet."""

from datetime import datetime
from dateutil.relativedelta import relativedelta
from data_manager import DataManager
from flight_data import FlightData
from notification_manager import NotificationManager

# NOTE: commented code of FlightSearch is to be run only once to update the sheet with city IATA codes.
# from flight_search import FlightSearch
# flight_search = FlightSearch()

data_mng = DataManager()

sheet_data = data_mng.get_rows()
sheet_data_length = len(sheet_data)
notifier = NotificationManager()

# for i in range(2, len(sheet_data) + 2):
#     data_mng.update_data(
#     "iataCode", flight_search.get_code(sheet_data[i - 2]["city"])["city"]["code"], i
# )

flight_data = FlightData()
date_from = datetime.now().strftime("%d/%m/%Y")
date_to = (datetime.today().date() + relativedelta(months=6)).strftime("%d/%m/%Y")
return_from = (datetime.today().date() + relativedelta(days=7)).strftime("%d/%m/%Y")
return_to = (datetime.today().date() + relativedelta(days=28)).strftime("%d/%m/%Y")

params = {
    "date_from": date_from,
    "date_to ": date_to,
    "return_from": return_from,
    "return_to": return_to,
}
search_results = []

for i in range(sheet_data_length):
    param = params.copy()
    param.update({"fly_to": sheet_data[i - 2]["iataCode"]})
    results = flight_data.search_flight_price(params=param)
    search_results.append(results)

for i in range(sheet_data_length):
    lowest_price = sheet_data[i]["lowestPrice"]
    current_price = search_results[i]["price"]
    if current_price < lowest_price:
        notifier.send_notification(search_results[i])
        break
