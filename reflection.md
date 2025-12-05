# Reflection for ISM2411 Data Cleaning Project
## What Copilot Generated
GitHub Copilot helped generate two main functions in my `data_cleaning.py` script:

1. `load_data(file_path: str)` – Copilot suggested the basic structure to read a CSV file using pandas.
2. `clean_column_names(df)` – Copilot suggested the approach to standardize column names (lowercase, replace spaces with underscores).

I triggered Copilot by writing comments describing the function purpose and starting the function definition. I then reviewed its suggestions and accepted them with some modifications.

## What I Modified
After Copilot's suggestions, I made several changes:

- Renamed some columns (e.g., 'qty' instead of 'quantity') to match the CSV file.
- Converted `price` and `qty` columns to numeric values, coercing errors to NaN to handle strings in numeric columns.
- Added the `clean_text_columns(df)` function to strip whitespace, remove quotes, and fix multiple spaces in text columns.
- Modified the logic in `handle_missing_values(df)` to fill missing values with 0 consistently.
- Made sure that the cleaning pipeline could handle both numeric and text columns correctly without errors.

## What I Learned
Through this project, I learned:

- How to clean real-world data in Python using pandas: standardizing column names, handling missing values, converting data types, and removing invalid rows.
- Copilot is a helpful tool for generating code structure quickly, but it requires review and adaptation to fit the actual dataset.
- For example, Copilot did not know the CSV had extra spaces or quotes in text columns, so I had to write `clean_text_columns` to fully clean the data.
- Using comments and structured prompts with Copilot improves the quality of suggestions and helps me learn best practices while coding.

Overall, this project helped me understand how to combine AI-assisted coding with careful human review to produce clean and reliable datasets.
