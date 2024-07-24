import pandas as pd
import numpy as np

# Load the uploaded CSV file
file_path = "planetary_positions_minute_by_minute_new.csv"
data = pd.read_csv(file_path)

# Define the planetary speed hierarchy
planets = ['Moon Position', 'Mercury Position', 'Venus Position', 'Sun Position', 'Mars Position', 'Jupiter Position', 'Saturn Position']
speed_hierarchy = {planet: idx for idx, planet in enumerate(planets)}

# Function to calculate angle differences following the speed hierarchy
def calculate_angle_difference(df, planet1, planet2):
    angle_diff = np.abs(df[planet1] - df[planet2])
    angle_diff = np.where(angle_diff > 180, 360 - angle_diff, angle_diff)  # Normalize the angle difference within 0-180 degrees
    if speed_hierarchy[planet1] < speed_hierarchy[planet2]:
        return angle_diff
    else:
        return -angle_diff

# Calculate the angle differences between all pairs of planets
angle_diffs = {}
for i in range(len(planets)):
    for j in range(i+1, len(planets)):
        planet1 = planets[i]
        planet2 = planets[j]
        angle_diffs[f'{planet1} vs {planet2}'] = calculate_angle_difference(data, planet1, planet2)

# Add angle differences to the dataframe
angle_diff_df = pd.DataFrame(angle_diffs)
result = pd.concat([data['DateTime'], angle_diff_df], axis=1)

# Define the output file path
output_file_path = "planetary_angle_differences.csv"

# Write the result to a CSV file
result.to_csv(output_file_path, index=False)

# Display the resulting dataframe (optional)
# print(result.head())
import pandas as pd
import numpy as np

# Load the uploaded CSV file
file_path = "planetary_positions_minute_by_minute_new.csv"
data = pd.read_csv(file_path)

# Define the planetary speed hierarchy
planets = ['Moon Position', 'Mercury Position', 'Venus Position', 'Sun Position', 'Mars Position', 'Jupiter Position', 'Saturn Position']
speed_hierarchy = {planet: idx for idx, planet in enumerate(planets)}

# Function to calculate angle differences following the speed hierarchy
def calculate_angle_difference(df, planet1, planet2):
    angle_diff = np.abs(df[planet1] - df[planet2])
    angle_diff = np.where(angle_diff > 180, 360 - angle_diff, angle_diff)  # Normalize the angle difference within 0-180 degrees
    if speed_hierarchy[planet1] < speed_hierarchy[planet2]:
        return angle_diff
    else:
        return -angle_diff

# Calculate the angle differences between all pairs of planets
angle_diffs = {}
for i in range(len(planets)):
    for j in range(i+1, len(planets)):
        planet1 = planets[i]
        planet2 = planets[j]
        angle_diffs[f'{planet1} vs {planet2}'] = calculate_angle_difference(data, planet1, planet2)

# Add angle differences to the dataframe
angle_diff_df = pd.DataFrame(angle_diffs)
result = pd.concat([data['DateTime'], angle_diff_df], axis=1)

# Define the output file path
output_file_path = "planetary_angle_differences.csv"

# Write the result to a CSV file
result.to_csv(output_file_path, index=False)

# Display the resulting dataframe (optional)
# print(result.head())
