"""Module to get the flight data within 6 months"""
import requests


class FlightData:
    """Class to get flight data within given period.
    This class is responsible for structuring the flight data."""

    def __init__(self) -> None:
        self.url = "https://tequila-api.kiwi.com/v2/search"
        self.fly_from = "LON"
        self.api_key = "n7xk0bryFDGEsUwuc20khcrcwkqZjdn6"

    def search_flight_price(self, params: dict):
        """Search for flights within the given time period

        Args:
            params = {
                fly_to (str): _description_
                date_from (str): _description_
                date_to (str): _description_
                return_from (str): _description_
                return_to (str): _description_
                }
        """
        params = {
            "fly_from": self.fly_from,
            "fly_to": params.get("fly_to"),
            "date_from": params.get("date_from"),
            "date_to": params.get("date_to"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "curr": "GBP",
        }

        headers = {"apikey": self.api_key}

        response = requests.get(self.url, params=params, headers=headers)

        json_response = response.json().get("data")[0]
        return {
            "city_to": json_response.get("cityTo"),
            "fly_to": json_response.get("flyTo"),
            "price": json_response.get("price"),
            "arrival": json_response.get("utc_arrival"),
            "departure": json_response.get("utc_departure"),
        }
