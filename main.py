# import math
# import threading
# import time
#
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
#
# chrome_driver_path = "/home/amey/Development/chromedriver"
#
# service = Service(executable_path=chrome_driver_path)
# driver = webdriver.Chrome(service=service)
#
# driver.get("https://orteil.dashnet.org/cookieclicker/")
#
# time.sleep(10)
# cookie = driver.find_element(by=By.CSS_SELECTOR, value="#bigCookie")
# cursor = driver.find_element(by=By.CSS_SELECTOR, value="#product0")
# grandma = driver.find_element(by=By.CSS_SELECTOR, value="#product1")
# farm = driver.find_element(by=By.CSS_SELECTOR, value="#product2")
# product3 = driver.find_element(by=By.CSS_SELECTOR, value="#product3")
# product4 = driver.find_element(by=By.CSS_SELECTOR, value="#product4")
# products = [
#     cursor,
#     grandma,
#     farm,
#     product3,
#     product4,
# ]
#
#
# def play():
#     cookie.click()
#
#
# def buy_product():
#     score = (
#         driver.find_element(by=By.CSS_SELECTOR, value="#cookies")
#         .text.split()[0]
#         .split(",")
#     )
#     score = int("".join(score))
#     cursor_price = driver.find_element(
#         by=By.CSS_SELECTOR, value="#productPrice0"
#     ).text.split(",")
#     cursor_price = int("".join(cursor_price))
#     grandma_price = driver.find_element(
#         by=By.CSS_SELECTOR, value="#productPrice1"
#     ).text.split(",")
#     grandma_price = int("".join(grandma_price))
#     farm_price = driver.find_element(by=By.CSS_SELECTOR, value="#productPrice2")
#     if farm_price:
#         farm_price = farm_price.text.split(",")
#         if farm_price[0] != "":
#             farm_price = int("".join(farm_price))
#         else:
#             farm_price = 0
#     product3_price = driver.find_element(by=By.CSS_SELECTOR, value="#productPrice3")
#     if product3_price:
#         product3_price = product3_price.text.split(",")
#         if product3_price[0] != "":
#             product3_price = int("".join(product3_price))
#         else:
#             product3_price = 0
#     product4_price = driver.find_element(by=By.CSS_SELECTOR, value="#productPrice4")
#     if product4_price:
#         product4_price = product4_price.text.split(",")
#         if product4_price[0] != "":
#             product4_price = int("".join(product4_price))
#         else:
#             product4_price = 0
#
#     prices = [
#         price
#         for price in [
#             cursor_price,
#             grandma_price,
#             farm_price,
#             product3_price,
#             product4_price,
#         ]
#         if price < score
#     ]
#     max_price = max(prices) if len(prices) > 0 else math.inf
#     if score > max_price:
#         products[prices.index(max_price)].click()
#
#
# while True:
#     play()
#     threading.Timer(5.0, buy_product).start()

from selenium import webdriver
from selenium.webdriver.common.by import By

import threading

from selenium.webdriver.chrome.service import Service

chrome_driver_path = "/home/amey/Development/chromedriver"

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.get("https://orteil.dashnet.org/cookieclicker/")

cookie = driver.find_element(By.ID, "bigCookie")


def buy_stuff():
    threading.Timer(30, buy_stuff).start()
    upgrades_prices = driver.find_elements(By.CSS_SELECTOR, ".upgrade.enabled")
    if upgrades_prices:
        upgrades_prices[-1].click()

    products_prices = driver.find_elements(By.CSS_SELECTOR, ".product.enabled")
    if products_prices:
        products_prices[-1].click()


buy_stuff()
while True:
    cookie.click()
