import os

import requests


class FlightSearch:
    """This class is responsible for talking to the Flight Search API."""

    def __init__(self) -> None:
        self.url = "https://tequila-api.kiwi.com/locations/query"
        self.api_key = os.getenv("TEQUILA_FLIGHT_KEY")

    def get_code(self, term):
        """Get the IATA code for the given location

        Args:
            term: The term to search for, must be one or more of 'id, name or code' of location
        """
        headers = {"apikey": self.api_key}

        params = {"term": term, "location_types": "airport"}

        response = requests.get(self.url, params=params, headers=headers)

        return response.json().get("locations")[0]
