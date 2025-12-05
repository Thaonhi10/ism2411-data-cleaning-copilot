# Data cleaning script for ISM2411 project
# This script loads raw sales data, cleans it, and outputs a processed CSV

import pandas as pd

# --- Function 1: Load data ---
def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.
    
    Input:
        file_path (str): path to the raw CSV file
    Output:
        pd.DataFrame: raw data loaded into a DataFrame
    """
    df = pd.read_csv(file_path)
    return df

# --- Function 2: Clean column names ---
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names by:
        - stripping leading/trailing whitespace
        - converting to lowercase
        - replacing spaces with underscores
    """
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

# --- Function 3: Handle missing values ---
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert price and qty columns to numeric, coercing errors to NaN,
    then fill missing values with 0.
    """
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
    df['qty'] = pd.to_numeric(df['qty'], errors='coerce').fillna(0)
    return df

# --- Function 4: Remove invalid rows ---
def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows where numeric values are clearly invalid:
        - price < 0
        - qty < 0
    """
    df = df[(df['price'] >= 0) & (df['qty'] >= 0)]
    return df

# --- Function 5: Clean text columns ---
def clean_text_columns(df: pd.DataFrame):
    """
    Strip whitespace and extra quotes from string columns like prodname and category.
    """
    text_cols = ['prodname', 'category', 'date_sold']
    for col in text_cols:
        df.loc[:, col] = df[col].astype(str).str.strip()                   # remove leading/trailing spaces
        df.loc[:, col] = df[col].str.replace('"', '')                      # remove quotes
        df.loc[:, col] = df[col].str.replace(r'\s+', ' ', regex=True)      # replace multiple spaces with single
    return df


# --- Main block to run the cleaning pipeline ---
if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    # Step 1: Load raw data
    df_raw = load_data(raw_path)

    # Step 2: Standardize column names
    df_clean = clean_column_names(df_raw)

    # Step 3: Handle missing values
    df_clean = handle_missing_values(df_clean)

    # Step 4: Remove invalid rows
    df_clean = remove_invalid_rows(df_clean)

    # Step 5: Clean text columns
    df_clean = clean_text_columns(df_clean)

    # Step 6: Save cleaned data
    df_clean.to_csv(cleaned_path, index=False)

    print("Cleaning complete. First few rows:")
    print(df_clean.head())
