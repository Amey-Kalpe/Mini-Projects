"""Module to manage data in Google Sheets using Sheety
"""

import requests


class DataManager:
    """This class is responsible for talking to the Google Sheet."""

    def __init__(self) -> None:
        self.app_id = "MzZlYjgzMDU="
        self.api_key = "MDk1NTFjMmYxNjIzYjQ3ODVkOWVjZGY0OTVmNDBiN2E="
        self.add_row_sheety = (
            "https://api.sheety.co/1020b1ffdbc6032ec47ba6dd5c3beb3a/flightDeals/prices"
        )
        self.edit_row_sheety = (
            "https://api.sheety.co/1020b1ffdbc6032ec47ba6dd5c3beb3a/flightDeals/prices"
        )
        self.get_row_sheety = (
            "https://api.sheety.co/1020b1ffdbc6032ec47ba6dd5c3beb3a/flightDeals/prices"
        )

    def get_rows(self):
        """Get the data present in Flight Deals Google Sheet"""
        response = requests.get(self.get_row_sheety)
        return response.json().get("prices")

    def update_data(self, property_, data, row_id):
        """Update data in the flight search Google Sheet

        Args:
            property_ (str): The property of which value is to be updated
            data (str): The data to be updated with
            row_id (int): The id of the row to update
        """
        params = {"price": {property_: data}}
        response = requests.put(self.edit_row_sheety + f"/{row_id}", json=params)
        return response.status_code
