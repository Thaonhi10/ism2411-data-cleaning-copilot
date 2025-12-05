# Data cleaning script for ISM2411 project
# Function to load CSV data into a pandas DataFrame
# Input: file path as a string
# Output: pandas DataFrame containing the raw data
import pandas as pd

def load_data(file_path: str):
    """
    Load a CSV file into a pandas DataFrame.
    """
    df = pd.read_csv(file_path)
    return df
