# Flight Deals Finder

### Find flight deals at low prices for a set of to and from locations. Get notified if a flight deal lower than the set threshold is found.

## APIs Required

- Google Sheet Data Management - https://sheety.co/

- Kiwi Partners Flight Search API (Free Signup, Requires Credit Card Details) - https://partners.kiwi.com/

- Tequila Flight Search API Documentation - https://tequila.kiwi.com/portal/docs/tequila_api

- Twilio SMS API - https://www.twilio.com/docs/sms

## Functionality

- FlightSearch (refer flight_search.py) uses the Kiwi Flight Search API to get the IATA codes for a particular city.
- The city names are fetched from a google sheet [(sample)](https://docs.google.com/spreadsheets/d/1YMK-kYDYwuiGZoawQy7zyDjEIU9u8oggCV4H2M9j7os/edit?usp=sharing) using the Sheety API.
- The IATA codes are filled in the IATA Code column in the google sheet.
- Use the fly_from attribute from the FlightData class (refer flight_data.py) to set the start location.
- The Kiwi Flight search API is used to check the cheapest flights from tomorrow to 6 months later.
- If a deal less than the threshold set in the google sheet is found, an SMS is sent with the flight details (refer notification_manager.py).

## Environment Variables To Be Set

- TWILIO_ACCOUNT_SID (Twilio Account ID)
- TWILIO_AUTH_TOKEN (Twilio Authentication Token)
- EDIT_ROW_SHEETY (Sheety API URL to edit row in google sheet)
- GET_ROW_SHEETY (Sheety API URL to fetch row in google sheet)
- TEQUILA_FLIGHT_KEY (API Key for Kiwi Flight Search API)

## How To Run

- Set all environment variables.
- Run `main.py` in a terminal.

