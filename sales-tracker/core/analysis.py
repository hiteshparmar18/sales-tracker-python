import numpy as np
import pandas as pd

def load_sales_data(file_path):
    """
    Load CSV data and return product names, sales data (NumPy array), and week labels.
    """
    df = pd.read_csv(file_path)
    df.fillna(0, inplace=True)  # Handle missing values by filling with 0
    week_labels = df.iloc[:, 0].tolist()
    product_names = df.columns[1:].tolist()
    sales_data = df.iloc[:, 1:].to_numpy()
    return product_names, sales_data, week_labels

def get_total_sales(data):
    """
    Return total sales for each product.
    """
    return np.sum(data, axis=0)

def get_best_seller(total_sales):
    """
    Return index of the best-selling product.
    """
    return int(np.argmax(total_sales))

def get_growth(data):
    """
    Return weekly growth (difference between weeks) for each product.
    """
    return np.diff(data, axis=0)

def get_percentage_growth(data):
    """
    Return weekly percentage growth for each product.
    """
    previous = data[:-1, :]
    next = data[1:, :]
    with np.errstate(divide='ignore', invalid='ignore'):
        growth = ((next - previous) / previous) * 100
        growth[np.isnan(growth)] = 0  # Handle divide by zero
    return growth

def get_weekly_totals(data):
    """
    Return total sales for each week across all products.
    """
    return np.sum(data, axis=1)