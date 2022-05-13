"""Notify user if flight price is at the lowest
"""

import os
from twilio.rest import Client


class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""

    def __init__(self) -> None:
        self.account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        self.auth_token = os.environ["TWILIO_AUTH_TOKEN"]

    def send_notification(self, journey_details):
        """Send notification about the journey

        Args:
            journey_details (dict): details of flight
        """
        message = f"Low Price Alert!! Only £{journey_details.get('price')} to fly from London-STN to {journey_details.get('city')}-{journey_details.get('airport')}, from {journey_details.get('arr')}"
        client = Client(self.account_sid, self.auth_token)
        message = client.messages.create(
            body=message,
            from_="+16625063427",
            to="+918149970187",
        )
