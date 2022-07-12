"""Module to manage data in Google Sheets using Sheety"""

import os
import requests


class DataManager:
    """This class is responsible for talking to the Google Sheet using Sheety API."""

    def __init__(self) -> None:
        self.edit_row_sheety = os.getenv("EDIT_ROW_SHEETY")
        self.get_row_sheety = os.getenv("GET_ROW_SHEETY")

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
