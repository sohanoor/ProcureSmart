import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from sklearn.linear_model import LinearRegression
import numpy as np
import openpyxl

# Configuration
EXCEL_FILE = 'local_sales_data.xlsx'
VENDOR_URL = 'NISA LOCAL'
USERNAME = '***********'
PASSWORD = '***********'
CHROME_DRIVER_PATH = 'chromedriver'

# Data Collection from Excel
def load_sales_data():
    df = pd.read_excel(EXCEL_FILE, sheet_name='SalesData')
    return df

# Selenium Web Automation
def get_vendor_data():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode for automation
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(VENDOR_URL)
    
    # Login
    driver.find_element(By.NAME, 'username').send_keys(USERNAME)
    driver.find_element(By.NAME, 'password').send_keys(PASSWORD)
    driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
    
    # Wait for login to complete and navigate to offers page
    driver.implicitly_wait(10)  # seconds
    offers_data = driver.find_element(By.ID, 'offers_table').text
    
    # Extract product list and prices
    product_data = driver.find_element(By.ID, 'product_list').text
    driver.quit()
    
    return offers_data, product_data

# Data Comparison
def compare_prices(sales_df, offers_df):
    # Assuming offers_df is a DataFrame with 'Product' and 'Price' columns
    merged_df = pd.merge(sales_df, offers_df, on='Product', how='left')
    merged_df['Best_Price'] = merged_df[['Price', 'Offer_Price']].min(axis=1)
    return merged_df

# Predict Product Quantity
def predict_quantity(sales_df):
    # Prepare data for prediction
    X = np.array(range(len(sales_df))).reshape(-1, 1)  # Time series index
    y = sales_df['Sales'].values
    model = LinearRegression().fit(X, y)
    next_week = np.array([[len(sales_df) + 1]])
    predicted_quantity = model.predict(next_week)
    return predicted_quantity

# Create Order List
def create_order_list(merged_df, predicted_quantity):
    order_df = merged_df[merged_df['Best_Price'].notna()]
    order_df['Order_Quantity'] = predicted_quantity
    return order_df[['Product', 'Order_Quantity', 'Best_Price']]

# Save to Excel
def save_to_excel(order_df):
    with pd.ExcelWriter(EXCEL_FILE, mode='a', engine='openpyxl') as writer:
        order_df.to_excel(writer, sheet_name='OrderList')

# Main Execution
def main():
    sales_df = load_sales_data()
    offers_data, product_data = get_vendor_data()
    
    # Convert data to DataFrame
    offers_df = pd.read_csv(pd.compat.StringIO(offers_data))  # Adjust parsing as needed
    product_df = pd.read_csv(pd.compat.StringIO(product_data))  # Adjust parsing as needed
    
    merged_df = compare_prices(sales_df, offers_df)
    predicted_quantity = predict_quantity(sales_df)
    order_df = create_order_list(merged_df, predicted_quantity)
    
    save_to_excel(order_df)
    print("Order list has been saved to Excel.")

if __name__ == '__main__':
    main()
