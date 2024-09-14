from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# website = 'https://www.audible.co.uk/search'
website = 'https://www.audible.co.uk/adblbestsellers'

chrome_driver_path = 'C:\\Users\\'USER'\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'


options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # browser is gone
options.add_argument("--remote-debugging-port=9222")
options.add_experimental_option("detach", True)

service = Service(executable_path=chrome_driver_path)

driver = webdriver.Chrome(service=service, options=options)
driver.get(website)
# driver.set_window_size(1920, 1080)
# driver.maximize_window()

# pagination
pagination = driver.find_element(By.XPATH, './/ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME, 'li')
last_page = int(pages[-2].text)

current_page = 1

book = []
author = []
length = []

while current_page <= last_page:
    # time.sleep(5)
    container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container ')))
    # container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container ')
    products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/li[contains(@class, "productListItem")]')))
    # products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')

    for product in products:
        b = product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text
        book.append(b)
        author.append(product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text)
        length.append(product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)
        print(b)

    current_page = current_page + 1
    try:
        next_page = driver.find_element(By.XPATH, '//span[contains(@class, "nextButton")]')
        next_page.click()
    except:
        pass

df = pd.DataFrame({'title': book, 'author': author, 'runtime': length})
df.to_csv('books.csv', index=False)

driver.quit()
