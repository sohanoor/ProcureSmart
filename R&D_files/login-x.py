from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
import time

website = 'https://twitter.com/'

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
cookies = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div[2]/div[1]/div')
cookies.click()
time.sleep(2)
sign_in_btn = driver.find_element(By.XPATH, '//a[@href="/login"]')
# login_btn = driver.find_element(By.XPATH, '//a[@href="/i/flow/signup"]')
sign_in_btn.click()
time.sleep(2)

username = driver.find_element(By.XPATH, '//input[@name="text"]')
username.send_keys('EMAIL')
time.sleep(2)
next_btn = driver.find_element(By.XPATH, '//div[@role="button"]//span[text()="Next"]')
next_btn.click()
time.sleep(2)

password = driver.find_element(By.XPATH, '//input[@autocomplete ="current-password"]')
password.send_keys('PASSWORD')
time.sleep(2)

login_button = driver.find_element(By.XPATH, '//div[@role="button"]//span[text()="Log in"]')
login_button.click()

# driver.quit()
