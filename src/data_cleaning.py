# Data cleaning script for ISM2411 project
# This script loads raw sales data, cleans it, and outputs a processed CSV

import pandas as pd
import numpy as np

# --- Function 1: Load data ---
def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    What: Reads the raw sales CSV from the given path.
    Why: We need to bring raw data into Python for cleaning and processing.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded data from {file_path}")
        print(f"Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return pd.DataFrame()  # Return empty DataFrame for error handling
    except Exception as e:
        print(f"Error loading file: {e}")
        return pd.DataFrame()

# --- Function 2: Clean column names ---
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names.

    What: Strip whitespace, lowercase all letters, replace spaces with underscores.
    Why: Inconsistent column names can cause errors in processing and analysis.
    """
    df = df.copy()  # Work on a copy to avoid warnings
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    print("Column names cleaned")
    return df

# --- Function 3: Handle missing values and invalid numbers ---
def handle_missing_and_invalid(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert numeric columns, handle missing or invalid values.

    What:
        - Convert 'price' and 'qty' to numeric, coercing errors.
        - Replace missing prices with median price.
        - Replace missing qty with 1.
        - Convert negative qty to positive (treat as returned items).
        - Replace zero or negative prices with median price.
        - Convert 'date_sold' to datetime and fill missing dates forward.
    Why:
        - Ensure all numeric columns are valid for analysis.
        - Maintain data integrity for sales calculations.
    """
    df = df.copy()  # Work on a copy
    
    # Convert numeric columns
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['qty'] = pd.to_numeric(df['qty'], errors='coerce')
    
    # Fill missing or invalid price with median
    median_price = df['price'].median()
    df.loc[:, 'price'] = df['price'].fillna(median_price)
    df.loc[df['price'] <= 0, 'price'] = median_price
    
    # Fill missing qty with 1 and make negative qty positive
    df.loc[:, 'qty'] = df['qty'].fillna(1).abs()
    
    # Convert date_sold to datetime, forward fill missing dates
    df.loc[:, 'date_sold'] = pd.to_datetime(df['date_sold'], errors='coerce')
    df.loc[:, 'date_sold'] = df['date_sold'].ffill()
    
    # Drop rows where date_sold is still missing
    initial_rows = len(df)
    df = df.dropna(subset=['date_sold'])
    removed_rows = initial_rows - len(df)
    if removed_rows > 0:
        print(f"Removed {removed_rows} rows with missing date_sold")
    
    print("Missing and invalid values handled")
    return df

# --- Function 4: Clean text columns ---
def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize text columns (prodname, category).

    What:
        - Strip whitespace
        - Remove quotes
        - Replace multiple spaces with a single space
        - Convert to title case
    Why:
        - Ensure product names and categories are consistent for grouping and analysis.
    """
    df = df.copy()  # Work on a copy
    
    text_cols = ['prodname', 'category']
    for col in text_cols:
        if col in df.columns:
            df.loc[:, col] = (
                df[col].astype(str)
                      .str.strip()
                      .str.replace('"', '')
                      .str.replace(r'\s+', ' ', regex=True)
                      .str.title()
            )
    
    print("Text columns cleaned")
    return df

# --- Function 5: Remove duplicates by grouping ---
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group identical products (same prodname, category, price, date_sold)
    and sum their quantities.

    What: Merge duplicate rows for accurate sales totals.
    Why: Raw data may have multiple entries for the same product on the same day.
    """
    initial_rows = len(df)
    
    # Make sure date_sold is in string format for grouping if it's datetime
    df_group = df.copy()
    
    # Group by relevant columns
    df_group = df_group.groupby(
        ['prodname', 'category', 'price', 'date_sold'], 
        as_index=False
    )['qty'].sum()
    
    removed_duplicates = initial_rows - len(df_group)
    print(f"Removed {removed_duplicates} duplicate rows by grouping")
    
    return df_group

# --- Additional Function: Data validation report ---
def generate_validation_report(df: pd.DataFrame) -> None:
    """
    Generate a simple validation report for the cleaned data.
    """
    print("\n=== DATA VALIDATION REPORT ===")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print("\nColumn names and data types:")
    print(df.dtypes)
    print("\nMissing values per column:")
    print(df.isnull().sum())
    print("\nBasic statistics:")
    print(df[['price', 'qty']].describe())

# --- Main block to run the cleaning pipeline ---
if __name__ == "__main__":
    # Define file paths
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"
    
    print("Starting data cleaning pipeline...")
    print("=" * 50)
    
    # Step 1: Load raw data
    df = load_data(raw_path)
    
    if df.empty:
        print("No data loaded. Exiting...")
        exit()
    
    print(f"Initial data shape: {df.shape}")
    print("\nInitial columns:")
    print(df.columns.tolist())
    
    # Step 2: Standardize column names
    df = clean_column_names(df)
    
    # Step 3: Clean text columns
    df = clean_text_columns(df)
    
    # Step 4: Handle missing and invalid numeric values
    df = handle_missing_and_invalid(df)
    
    # Step 5: Remove duplicate rows by grouping
    df = remove_duplicates(df)
    
    # Step 6: Sort by date for better readability
    df = df.sort_values('date_sold', ascending=True).reset_index(drop=True)
    
    # Step 7: Generate validation report
    generate_validation_report(df)
    
    # Step 8: Save cleaned data
    # Ensure the output directory exists
    import os
    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)
    
    df.to_csv(cleaned_path, index=False)
    print(f"\nCleaned data saved to: {cleaned_path}")
    
    print("\n" + "=" * 50)
    print("Cleaning complete. First few rows:")
    print(df.head())
    
    # Optional: Show sample of cleaned data
    print("\nSample of cleaned data (5 random rows):")
    print(df.sample(5, random_state=42))

