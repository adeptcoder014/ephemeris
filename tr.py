import json
import gzip
from datetime import datetime
import math
import time

def load_compressed_json(file_path):
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        return json.load(f)

# Load compressed JSON files for Sun and Moon almanacs
DATA_FILE_MOON = './transit_data/transit_data_moon_data_compressed.json.json.gz'
DATA_FILE_SUN = './transit_data/transit_data_sun_data_compressed.json.json.gz'

moon_almanac = load_compressed_json(DATA_FILE_MOON)
sun_almanac = load_compressed_json(DATA_FILE_SUN)

# Desired angles to calculate
angles = [0,180.000]

# Initialize hashmap to keep track of found angles
found_angles = {angle: None for angle in angles}

# Function to calculate angle between two positions
def calculate_angle(position1, position2):
    angle = abs(position1 - position2)
    return angle

# Iterate through almanac data and calculate angles
for moon_entry in moon_almanac:
    moon_datetime = datetime.strptime(moon_entry["date"] + " " + moon_entry["time"], "%Y-%m-%d %H:%M:%S")
    moon_position = moon_entry["absolute_position"]
    
    for sun_entry in sun_almanac:
        sun_datetime = datetime.strptime(sun_entry["date"] + " " + sun_entry["time"], "%Y-%m-%d %H:%M:%S")
        sun_position = sun_entry["absolute_position"]
        
        current_angle = calculate_angle(moon_position, sun_position)
        rounded_angle = round((current_angle),4)
        
        if rounded_angle in angles and found_angles[rounded_angle] is None:
            print(f" =====================  MILA {rounded_angle} ===================================")
            # time.sleep(1)
            found_angles[rounded_angle] = {
                "angle": rounded_angle,
                "angle_diff": current_angle,
                
                "sun_position": sun_position,
                "moon_position": moon_position,
                "sun_datetime": sun_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "moon_datetime": moon_datetime.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Check if all angles are found
            all_found = all(found_angles[angle] is not None for angle in angles)
            if all_found:
                break
    else:
        continue
    break

# Write found results to a JSON file
output_file = 'found_angles.json'
with open(output_file, 'w') as f:
    json.dump(found_angles, f, indent=4)

print(f"Results written to {output_file}")

# Print results for all desired angles
for angle, found_data in found_angles.items():
    if found_data:
        print(f"At {found_data['angle']} degrees: Sun position {found_data['sun_position']} at {found_data['sun_datetime']}")
    else:
        print(f"No data found for {angle} degrees")
