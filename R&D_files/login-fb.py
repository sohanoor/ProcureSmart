from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
import time

website = 'https://www.facebook.com/'

chrome_driver_path = 'E:\\DataAnalytics\\WebScrap\\seleniumLogin-X\\chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument("--remote-debugging-port=9222")
options.add_experimental_option("detach", True)

service = Service(executable_path=chrome_driver_path)

driver = webdriver.Chrome(service=service, options=options)
driver.get(website)
# driver.maximize_window()
print(driver.title)

time.sleep(2)

username = driver.find_element(By.XPATH, '//input[@name="email"]')
username.send_keys('EMAIL')
time.sleep(2)

password = driver.find_element(By.XPATH, '//input[@name="pass"]')
password.send_keys('PASS')
time.sleep(2)

login_button = driver.find_element(By.XPATH, '//button[@name="login"]')
login_button.click()

# driver.quit()
