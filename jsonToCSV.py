import pandas as pd

# Read the JSON file
json_file_path = './transit_data/transit_data_saturn_data_compressed.json.json'
df = pd.read_json(json_file_path)

# Write The DataFrame To a CSV file
csv_file_path = 'ephemeris/saturn.csv'
df.to_csv(csv_file_path, index=False)

print(f"JSON data has been successfully converted to CSV and saved to {csv_file_path}")
