import pandas as pd
import os

# Define the list of planets
planets = ['sun','moon','mercury', 'venus', 'mars', 'jupiter', 'saturn']

# Iterate over each planet
for planet in planets:
    # Read the JSON file
    json_file_path = f'./transit_data/transit_data_{planet}_data_compressed.json.json'
    df = pd.read_json(json_file_path)

    # Write the DataFrame to a CSV file
    csv_file_path = f'ephemerides/ephemeris/{planet}.csv'
    df.to_csv(csv_file_path, index=False)

    print(f"JSON data for {planet.capitalize()} has been successfully converted to CSV and saved to {csv_file_path}")
