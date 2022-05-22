from bs4 import BeautifulSoup
import lxml
import requests

url = "https://www.amazon.com/Instant-Pot-Pressure-Steamer-Sterilizer/dp/B08PQ2KWHS/"
headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    "Chrome/101.0.4951.64 Safari/537.36",
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "lxml")

price = soup.select_one(
    selector="td.a-span12 span.apexPriceToPay span.a-offscreen"
).getText()[1:]
