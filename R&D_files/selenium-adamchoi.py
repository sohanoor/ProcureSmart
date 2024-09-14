from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
import time

website = 'https://www.adamchoi.co.uk/overs/detailed'

chrome_driver_path = 'C:\\Users\\sohan\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument("--remote-debugging-port=9222")
options.add_experimental_option("detach", True)

service = Service(executable_path=chrome_driver_path)

driver = webdriver.Chrome(service=service, options=options)
driver.get(website)
print(driver.title)

all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click()

dropdown = Select(driver.find_element(By.ID, 'country'))
dropdown.select_by_visible_text('Spain')

time.sleep(3)  # wait for 3 sec

matches = driver.find_elements(By.TAG_NAME, 'tr')

date = []
home_team = []
score = []
away_team = []
count = 0

for match in matches:
    count = count + 1
    date.append(match.find_element(By.XPATH, './td[1]').text)  # '//tr/td[1]'
    home_team.append(match.find_element(By.XPATH, './td[2]').text)  # '//tr/td[2]'
    score.append(match.find_element(By.XPATH, './td[3]').text)  # '//tr/td[3]'
    away_team.append(match.find_element(By.XPATH, './td[4]').text)  # '//tr/td[4]'
    print(f'{count}: {match.find_element(By.XPATH, './td[2]').text}')

df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})
df.to_csv('football_data.csv', index=False)
print(df)

driver.quit()
