from flask import Flask, request, jsonify
import json
import gzip

app = Flask(__name__)

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

def load_compressed_json(file_path):
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        return json.load(f)

# Load your compressed JSON data at the start (or on request, depending on your use case)
DATA_FILE = 'compressed_file.json.gz'
data = load_compressed_json(DATA_FILE)

@app.route('/search', methods=['GET'])
def search_data():
    # Extract query parameters
    date = request.args.get('date')
    planet = request.args.get('planet')
    print('---------------------', planet)
    
    if not date or not planet:
        return jsonify({"error": "Please provide both 'date' and 'planet' parameters"}), 400
    
    # Search in the data
    results = [entry for entry in data if entry.get('date') == date and entry.get('name') == planet]
    
    if not results:
        return jsonify({"error": "No matching data found"}), 404
    
    # Calculate the average of 'absolute_position'
    total_absolute_position = sum(entry['absolute_position'] for entry in results)
    average_absolute_position = total_absolute_position / len(results)
    
    return jsonify({
        "count": len(results),
        "average_absolute_position": average_absolute_position,
        "results": results
    })

if __name__ == '__main__':
    app.run(debug=True)
