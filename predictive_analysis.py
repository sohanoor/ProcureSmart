import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load historical sales data
def load_data(file_path):
    df = pd.read_excel(file_path, sheet_name='SalesData')
    return df

# Prepare data for modeling
def prepare_data(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df['DayOfYear'] = df.index.dayofyear
    df['Year'] = df.index.year
    
    # Use 'DayOfYear' and 'Year' as features
    X = df[['DayOfYear', 'Year']]
    y = df['Sales']
    
    return X, y

# Train predictive model
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predict on test set
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    
    return model

# Predict future sales
def predict_future_sales(model, X):
    future_dates = pd.date_range(start='2024-01-01', periods=7, freq='W')
    future_df = pd.DataFrame({
        'DayOfYear': future_dates.dayofyear,
        'Year': future_dates.year
    })
    
    future_predictions = model.predict(future_df)
    future_df['Predicted_Sales'] = future_predictions
    
    return future_df

# Visualize predictions
def visualize_predictions(df, future_df):
    plt.figure(figsize=(12, 6))
    
    plt.plot(df.index, df['Sales'], label='Historical Sales', marker='o')
    plt.plot(future_df.index, future_df['Predicted_Sales'], label='Predicted Sales', marker='o', linestyle='--')
    
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.title('Sales Prediction')
    plt.legend()
    plt.grid(True)
    plt.show()

# Main execution
def main():
    file_path = 'sales_data.xlsx'
    df = load_data(file_path)
    X, y = prepare_data(df)
    model = train_model(X, y)
    future_df = predict_future_sales(model, X)
    visualize_predictions(df, future_df)
    print(f"Future sales predictions:\n{future_df}")

if __name__ == '__main__':
    main()
