import json
import gzip

def compress_json(input_file, output_file):
    # Read the JSON data from the file
    with open(input_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Serialize JSON data to a string
    json_str = json.dumps(json_data)

    # Compress the JSON string
    with gzip.open(output_file, 'wt', encoding='utf-8') as gz:
        gz.write(json_str)

# Example usage
input_file = 'transit_data_moon_minutely.json'
output_file = 'compressed_file.json.gz'
compress_json(input_file, output_file)


