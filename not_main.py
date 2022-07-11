from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

chrome_driver_path = "/home/amey/Development/chromedriver"

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

# driver.get("https://www.google.co.in")

driver.get("https://www.python.org/")

dates = driver.find_elements(by=By.CSS_SELECTOR, value=".event-widget time")

names = driver.find_elements(by=By.CSS_SELECTOR, value=".event-widget .menu a")

events = {
    i: {"time": "2022-" + dates[i].text, "names": names[i].text}
    for i in range(len(names))
}

print(events)

driver.quit()
