import pandas as pd

# Read the two CSV files
df1 = pd.read_csv('ephemeris/sun.csv')
df2 = pd.read_csv('ephemeris/moon.csv')

# Merge the two DataFrames on the date and time columns
merged_df = pd.merge(df1, df2, on=['date', 'time'], suffixes=('_1', '_2'))

# Function to calculate aspect based on absolute positions
def calculate_aspect(row):
    aspect = abs(row['absolute_position_1'] - row['absolute_position_2'])
    return aspect

# Apply the aspect calculation function and add the new column
merged_df['aspect'] = merged_df.apply(calculate_aspect, axis=1)

# Save the merged DataFrame with the aspect column to a new CSV file
merged_df.to_csv('sun_moon_aspects.csv', index=False)

# Print the resulting DataFrame
print(merged_df)
