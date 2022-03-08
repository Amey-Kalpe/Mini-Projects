import os
import requests
from twilio.rest import Client

# Download the helper library from https://www.twilio.com/docs/python/install

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_URL = "https://www.alphavantage.co/query"
stock_params = {
    "function": "GLOBAL_QUOTE",
    "symbol": STOCK,
    "apikey": "8Z2EKEYR6JWJ90HA",
}
stock = requests.get(STOCK_URL, params=stock_params)
stock_data = stock.json()
change_percent = float(stock_data.get("Global Quote").get("10. change percent")[:-1])

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]

if 5 <= change_percent <= -5:
    client = Client(account_sid, auth_token)

    NEWSAPI_URL = "https://newsapi.org/v2/everything"
    newsapi_params = {
        "apiKey": "09e35f286b2e4c3fba4c4bdf217adc73",
        "q": COMPANY_NAME,
        "pageSize": 3,
    }

    news = requests.get(NEWSAPI_URL, newsapi_params)
    news_data = news.json()
    articles = news_data.get("articles")

    for article in articles:
        if change_percent >= 5:
            news = f"TSLA: 🔺{int(change_percent)}\nTitle:\n{article.get('title')}\n\nDescription:\n{article.get('description')}\n\nRead here:\n{article.get('url')}"
        elif change_percent <= -5:
            news = f"TSLA: 🔻{int(change_percent)}\nTitle:\n{article.get('title')}\n\nDescription:\n{article.get('description')}\n\nRead here:\n{article.get('url')}"

        message = client.messages.create(
            body=news,
            from_="+16625063427",
            to="+918149970187",
        )
        print(message.status)
