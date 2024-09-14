from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd


website = 'https://www.audible.co.uk/search'

chrome_driver_path = 'C:\\Users\\sohan\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'
# chrome_driver_path = 'E:\\DataAnalytics\\WebScrap\\seleniumMultipage-Audible\\chromedriver.exe'''

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # browser is gone
options.add_argument("--remote-debugging-port=9222")
options.add_experimental_option("detach", True)

service = Service(executable_path=chrome_driver_path)

driver = webdriver.Chrome(service=service, options=options)
driver.get(website)
# driver.set_window_size(1920, 1080)
driver.maximize_window()
print(driver.title)

container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container ')
# products = container.find_element(By.XPATH, './li')
products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')
print(products)

book = []
author = []
length = []
for product in products:
    b = product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text
    book.append(b)
    author.append(product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text)
    length.append(product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)
    print(b)

df = pd.DataFrame({'title': book, 'author': author, 'runtime': length})
df.to_csv('books.csv', index=False)

driver.quit()
