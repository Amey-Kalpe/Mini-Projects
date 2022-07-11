from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "/home/amey/Development/chromedriver"

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

# driver.get("https://en.wikipedia.org/wiki/Main_Page")

# article_count = driver.find_element(by=By.CSS_SELECTOR, value="#articlecount a")
#
# print(article_count.text)

driver.get("http://secure-retreat-92358.herokuapp.com/")

first_name = driver.find_element(by=By.NAME, value="fName")
first_name.send_keys("Amey")

last_name = driver.find_element(by=By.NAME, value="lName")
last_name.send_keys("Kalpe")

email = driver.find_element(by=By.NAME, value="email")
email.send_keys("ameykalpe16@gmail.com")

submit = driver.find_element(by=By.CSS_SELECTOR, value="form button")
submit.click()

# driver.quit()
