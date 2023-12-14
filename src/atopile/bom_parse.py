# Load the newly provided CSV file to parse the capacitor values
#%%
import pandas as pd
import numpy as np
import re
#%%
components_csv_path = "/Users/narayanpowderly/Documents/atopile-workspace/atopile/src/atopile/Basic_Parts.csv"
components_df = pd.read_csv(components_csv_path)

# Define the function to parse the description and extract values with different units
def parse_description(description):
    # Initialize the default value
    value = None
    # Define the regex pattern to match the different units within the description
    patterns = {
        'pF': 1e-12,
        'nF': 1e-9,
        'µF': 1e-6,
        'uF': 1e-6, # Some descriptions might use 'u' instead of the micro symbol
    }
    # Try to find each pattern and convert accordingly
    for unit, multiplier in patterns.items():
        match = re.search(r'(\d+(\.\d+)?)(?={})'.format(unit), description)
        if match:
            value = float(match.group(1)) * multiplier
            break
    return value

# Apply the parsing function to the 'Description' column to get values in Farads
components_df['value'] = components_df['Description'].apply(parse_description)

# Handle NaN for tolerance when it is not provided
components_df['tolerance'] = components_df['tolerance'].replace('', np.nan).astype(float)

# Calculate min_value and max_value columns using value and tolerance columns
components_df["min_value"] = components_df["value"] * (1 - components_df["tolerance"] / 100)
components_df["max_value"] = components_df["value"] * (1 + components_df["tolerance"] / 100)

# Display the head of the dataframe to ensure the changes are correct
# components_df.head()

# %%
components_df.head(20)