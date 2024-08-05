from flask import Flask, request
import swisseph as swe
import requests
from util import get_planet_position, get_degree_minute_zodiac, get_moon_position, zodiacData, get_houses_position, get_planet_by_date_time,getPlanetsByDate,load_compressed_json

import sys
import time
import logging
 
from flask_cors import CORS
import json

# ==============================================================================

app = Flask(__name__)
CORS(app)


# ===========================================================
@app.route('/')
def home():
    message = "<h1> Welcome to Ephemeris APIs 🗓️ <h1/>"
    return message
# ==============================================================================


@app.route('/planets', methods=['POST'])
def optimize_get():

    data = request.json['value']
    print(f"--- data -----", data)
    # print( f"--- data ----- {data}")
    lat = data['location']['lat']
    long = data['location']['long']
    timeOfBirth = data['time']
    date = data['dob']

    planets = [
        swe.MOON,
        swe.MERCURY,
        swe.VENUS,
        swe.SUN,
        swe.MARS,
        swe.JUPITER,
        swe.SATURN,
        swe.MEAN_NODE]
    message = []

    for planet in planets:
        planet_pos = get_planet_position(planet, lat, long, date, timeOfBirth)
        degree, zodiac, minute = get_degree_minute_zodiac(planet_pos)
   

        message.append({
            'name': swe.get_planet_name(planet).lower(),
            'position': {
                'degree': degree,
                "minute": minute,
                'sign': zodiacData[zodiac]['sign'],
                'name': zodiacData[zodiac]['name']
            }
        })

    return {
        "status": 200,
        "data": message
    }

# ==============================================================================


@app.route('/houses', methods=['POST'])
def get_houses():
   
    data = request.json
    fetched_location = data['location']
    date = data['date']
    time = data['time']
    # long = data['long']
    # date = data['date']
    # timeOfBirth = data['time']
    location_detail = city_position_obj[fetched_location]
   
    positions = get_houses_position(
        location_detail['latitude'],
        location_detail['longitude'],
        date,
        time,
        location_detail['astral_value'][2],
        location_detail['astral_value'][3]
        )[0]
    # ayanamsha = get_houses_position()[1]
    houses = []
    for pos in positions:
        degree, zodiac, minute = get_degree_minute_zodiac(pos)
        data = f"{degree}° {zodiacData[zodiac]['sign']} {round(minute)}'"
        houses.append({
            "name": zodiacData[zodiac]['name'],
            "houseNumber": zodiacData[zodiac]['serial'],
            "houseSign": zodiacData[zodiac]['sign'],
            "position": data,
        })

    return {
        "status": 200,
        "data": houses,
    }
# ==============================================================================

@app.route('/get-moon')
def get_moon():

    message = []

    planet_pos = get_moon_position()
    degree, zodiac, minute = get_degree_minute_zodiac(planet_pos)
    message.append({
        'position': f"{degree}° {zodiacData[zodiac]['sign']} {round(minute)}'"
    })

    return {
        "status": 200,
        "data": message
    }


# ==============================================================================

@app.route('/get-planet-byDateTime', methods=['POST'])
def get_planet_byDateTime():
    date = request.json['date']
    print(date,"===============   ========================")
    time = request.json['time']

    planets = [
        swe.MOON,
        swe.MERCURY,
        swe.VENUS,
        swe.SUN,
        swe.MARS,
        swe.JUPITER,
        swe.SATURN,
        swe.MEAN_NODE]
    planetPositionForGivenDateTime = []

    for planet in planets:
        planet_pos = get_planet_by_date_time(planet,date,time)
        degree, zodiac, minute = get_degree_minute_zodiac(planet_pos)

        planetPositionForGivenDateTime.append({
            'name': swe.get_planet_name(planet).lower(),
            'absolutePosition':planet_pos,
            'position': {
                'degree': degree,
                "minute": minute,
                'sign': zodiacData[zodiac]['sign'],
                'name': zodiacData[zodiac]['name'],
            }
        })   

    return {
        "status": 200,
        "data": planetPositionForGivenDateTime
    }

# ==============================================================================

@app.route('/get-planet-byDateTime_d', methods=['POST'])
def get_planet_byDateTime_d():
    date = request.json['date']
    time = request.json['time']
    planet = request.json['planet']
    rashi = request.json['rashi']
    
    def handle_planet_swiss_value_from_name(planet_name):
        planet_swiss_value_obj={
            'venus':swe.VENUS,
            'moon':swe.MOON,
            'mercury':swe.MERCURY,
            'sun':swe.SUN,
            'mars':swe.MARS,
            'jupiter':swe.JUPITER,
            'saturn':swe.SATURN,
            'meanNode':swe.MEAN_NODE
        }
        if planet_name in planet_swiss_value_obj:
            return planet_swiss_value_obj[planet_name]
        else:
            return f"Error: {planet_name} is not a valid planet."

    planet_swiss_value = handle_planet_swiss_value_from_name(planet)
    
    

    
    planet_pos = get_planet_by_date_time(planet_swiss_value,date,time)
    
    degree, zodiac, minute = get_degree_minute_zodiac(planet_pos)
    
    specificPlanetPositionForGivenDateTime={
            'name': planet,
            'position': {
                'degree': degree,
                "minute": minute,
                'sign': zodiacData[zodiac]['sign'],
                'name': zodiacData[zodiac]['name'],
            }
        }

    return {
        "status": 200,
        "data": specificPlanetPositionForGivenDateTime
    }





@app.route('/transit-time', methods=['POST'])
def get_transit_time():
    data = request.json
    planet_name = data.get('planet', '').lower()
    rashi = data.get('rashi', '').lower()

    # Ensure valid planet and zodiac sign are provided
    if planet_name not in ['moon', 'mercury', 'venus', 'sun', 'mars', 'jupiter', 'saturn', 'mean_node'] :
        # or rashi not in zodiacData['zodiac']:
        return {"status": 400, "error": "Invalid planet or zodiac sign"}

    planet_swiss_value = getattr(swe, planet_name.upper())  # Get the Swiss Ephemeris value for the planet
    print('planet_swiss_value=--------',planet_swiss_value)

    # Get the transit time for the specified planet in the given zodiac sign
    transit_time = getPlanetsByDate(planet_swiss_value, rashi)

    return {
        "status": 200,
        "data": {
            "planet": planet_name,
            "transit_time": transit_time
        }
    }



# =================================

from flask import Flask, jsonify, request
from datetime import datetime
from astral.sun import sun
from astral import LocationInfo
import pytz

# app = Flask(__name__)

# Order of the planets in Chaldean sequence
planets = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]

# Mapping of days to ruling planets
day_ruler = {
    0: "Moon",     # Monday
    1: "Mars",     # Tuesday
    2: "Mercury",  # Wednesday
    3: "Jupiter",  # Thursday
    4: "Venus",    # Friday
    5: "Saturn",   # Saturday
    6: "Sun"       # Sunday
}

def mins2hoursandmins(time):
    hours = time // 60
    minutes = time % 60
    if minutes < 10:
        minutes = f"0{minutes}"
    return f"{hours}:{minutes}"

def getminutes4subtracting(start_time):
    minutes = int(start_time[-2:])
    minutes -= 1
    if minutes < 10:
        minutes = f"0{minutes}"
    return str(minutes)

def gethours(time):
    hours = time // 60
    return str(hours)

def get_planetary_hours(city, date):
    location = LocationInfo(city['astral_value'][0], city['astral_value'][1], city['astral_value'][2], city['latitude'], city['longitude'])
    
    # Calculate sunrise and sunset times
    s = sun(location.observer, date=date)
    timezone = pytz.timezone(location.timezone)
    sunrise = s['sunrise'].astimezone(timezone)
    sunset = s['sunset'].astimezone(timezone)
    
    # Length of day and night in hours
    sunrisehour, sunriseminute = sunrise.hour, sunrise.minute
    sunsethour, sunsetminute = sunset.hour, sunset.minute

    sunrisehourtominutes = sunrisehour * 60
    sunrisetotalminutes = sunrisehourtominutes + sunriseminute
    sunsethourtominutes = sunsethour * 60
    sunsettotalminutes = sunsethourtominutes + sunsetminute
    difference = sunsettotalminutes - sunrisetotalminutes

    length_of_hour = difference // 12
    array = [sunrisetotalminutes + i * length_of_hour for i in range(12)]

    # Determine order of the planets based on Chaldean sequence
    dayoftheweek = date.weekday()
    chaldean = planets.copy()

    if dayoftheweek == 0:
        chaldean = ["Moon", "Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury"]
    elif dayoftheweek == 1:
        chaldean = ["Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter"]
    elif dayoftheweek == 2:
        chaldean = ["Mercury", "Moon", "Saturn", "Jupiter", "Mars", "Sun", "Venus"]
    elif dayoftheweek == 3:
        chaldean = ["Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn"]
    elif dayoftheweek == 4:
        chaldean = ["Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars", "Sun"]
    elif dayoftheweek == 5:
        chaldean = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]
    elif dayoftheweek == 6:
        chaldean = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]

    # Repeat the sequence
    newchaldean = chaldean.copy()
    chaldean.extend(newchaldean)
    chaldean = chaldean[:-2]

    # Calculate end of hour and planetary hours
    planetary_hours = []
    j = 1
    for y in range(12):
        if y < 11:
            hh = gethours(array[j])
            mm = getminutes4subtracting(mins2hoursandmins(array[j]))
            hhmm = f"{hh}:{mm}"
        else:
            lastdayhour = array[-1] + length_of_hour - 1
            hhmm = mins2hoursandmins(lastdayhour)
        if y < 10:
            j += 1
        planetary_hours.append((mins2hoursandmins(array[y]), hhmm, chaldean[y]))
    return planetary_hours

city_position_obj={
    'london' : {
        'latitude' : 51.51,  
        'longitude' : -0.09  ,
        'astral_value':("London", "England", "Europe/London",1.00),
    },
     'delhi' : {
        'latitude' : 28.7041,  
        'longitude' : 77.1025,
        'astral_value':("Delhi", "India", "Asia/Kolkata",5.5)
    },
      'mumbai' : {
        'latitude' : 19.0760,  
        'longitude' : 72.8777 ,
        'astral_value':("Mumbai", "India", "Asia/Kolkata",5.5)
    },
       'lucknow' : {
        'latitude' : 26.8467,  
        'longitude' : 80.9462  ,
        'astral_value':("Lucknow", "India", "Asia/Kolkata",5.5)
    }
}
        
@app.route('/planetary-hours', methods=['GET'])
def get_planetary_hours_api():
    # city = request.json['city']
    city = request.args.get('city')
    date_str = request.args.get('date')
    # date_str = request.json['date']
    date = datetime.strptime(date_str, '%Y-%m-%d')
    # print('---- started -----', request.data)
    print('-----',date,city)

    if city not in city_position_obj:
        return jsonify({'error': 'City not found'}), 404

    hours = get_planetary_hours(city_position_obj[city], date)
    
    response_object = []
    for hour in hours : 
        response_object.append({
            'start':hour[0],
            'end':hour[1],
            'planet':hour[2]
        })
    return {
        "status": 200,
        "planetaryHours":response_object
    }

#






@app.route('/get-planet-transit-py', methods=['GET'])
def search_data():

    # date = request.args.get('date')
    planet = request.args.get('planet')
    
    DATA_FILE = f'./transit_data/transit_data_{planet}_data_compressed.json.json.gz'
    
    
    data = load_compressed_json(DATA_FILE)
    
    # Extract query parameters
    print('---------------------', get_degree_minute_zodiac(59.9998))
    
    # if not date or not planet:
    #     return jsonify({"error": "Please provide both 'date' and 'planet' parameters"}), 400
    
    # Search in the data
    results = [entry for entry in data if entry.get('name') == planet]
    
    if not results:
        return jsonify({"error": "No matching data found"}), 404
    
  
    ingress_degree=[0.00,30.00,60.00,90.00,120.00,150.00,180.00,210.00,240.00,270.00,300.00,330.00]
    # ingress_degree=[0,30,60,90,120,150,180,210,240,270,300,330]
    response_data=[]
    seen_positions = set()

    for result in results : 
        rounded_position = round(result['absolute_position'],3)
        rounded_position_moon = round(result['absolute_position'],2)

        if planet != 'moon' and rounded_position in ingress_degree and   rounded_position not in seen_positions:
            degree, zodiac, minute = get_degree_minute_zodiac(round(result['absolute_position']))
            response_data.append(
                {
                    "name": result['name'],
                    # 'absolute_position' : round(result['absolute_position']),
                    'absolute_position' : (result['absolute_position']),
                    "position":{
                        'degree':degree, 
                        'zodiac':zodiacData[zodiac]['sign'],
                        'zodiacName':zodiacData[zodiac]['name'],

                        'minute':minute
                        },
                    "date": result['date'],
                    "time":result['time']
                 })
            seen_positions.add(rounded_position)


# ========================================
        elif planet == 'moon' and rounded_position_moon in ingress_degree :
            degree, zodiac, minute = get_degree_minute_zodiac(round(result['absolute_position']))
            response_data.append(
                {
                    "name": result['name'],
                    # 'absolute_position' : round(result['absolute_position']),
                    'absolute_position' : (result['absolute_position']),
                    "position":{
                        'degree':degree, 
                        'zodiac':zodiacData[zodiac]['sign'],
                        'zodiacName':zodiacData[zodiac]['name'],
                        'minute':minute
                        },
                    "date": result['date'],
                    "time":result['time']
                 })

# ==================================
     
    return jsonify({
        "count": len(response_data),
        "data": response_data })

# =====================================

@app.route('/get-planet-transit', methods=['GET'])
def get_transit():

    # date = request.args.get('date')
    planet = request.args.get('planet')
    
    DATA_FILE = f'./transit_data/transit_data_{planet}_data_compressed.json.json.gz'
    
    
    data = load_compressed_json(DATA_FILE)
    
    # Extract query parameters
    print('---------------------', get_degree_minute_zodiac(59.9998))
    
    # if not date or not planet:
    #     return jsonify({"error": "Please provide both 'date' and 'planet' parameters"}), 400
    
    # Search in the data
    results = [entry for entry in data if entry.get('name') == planet]
    
    if not results:
        return jsonify({"error": "No matching data found"}), 404
    
  
    ingress_degree=[0.00,30.00,60.00,90.00,120.00,150.00,180.00,210.00,240.00,270.00,300.00,330.00]
    # ingress_degree=[0,30,60,90,120,150,180,210,240,270,300,330]
    response_data=[]
    seen_positions = set()

    for result in results : 
        rounded_position = round(result['absolute_position'],3)
        rounded_position_moon = round(result['absolute_position'],2)

        if planet != 'moon' and rounded_position in ingress_degree and   rounded_position not in seen_positions:
            degree, zodiac, minute = get_degree_minute_zodiac(round(result['absolute_position']))
            response_data.append(
                {
                    "name": result['name'],
                    # 'absolute_position' : round(result['absolute_position']),
                    'absolute_position' : (result['absolute_position']),
                    "position":{
                        'degree':degree, 
                        'zodiac':zodiacData[zodiac]['sign'],
                        'zodiacName':zodiacData[zodiac]['name'],

                        'minute':minute
                        },
                    "date": result['date'],
                    "time":result['time']
                 })
            seen_positions.add(rounded_position)


# ========================================
        elif planet == 'moon' and rounded_position_moon in ingress_degree :
            degree, zodiac, minute = get_degree_minute_zodiac(round(result['absolute_position']))
            response_data.append(
                {
                    "name": result['name'],
                    # 'absolute_position' : round(result['absolute_position']),
                    'absolute_position' : (result['absolute_position']),
                    "position":{
                        'degree':degree, 
                        'zodiac':zodiacData[zodiac]['sign'],
                        'zodiacName':zodiacData[zodiac]['name'],
                        'minute':minute
                        },
                    "date": result['date'],
                    "time":result['time']
                 })
            
     
    return jsonify({
        "count": len(response_data),
        "data": response_data })

# ==================================


import pandas as pd
# Load the CSV data into a DataFrame
# df = pd.read_csv('planetary_angle_differences.csv')
# df = pd.read_csv('planetary_positions_minute_by_minute_new.csv')

# Route to get all data
# @app.route('/data', methods=['GET'])
# def get_all_data():
#     date = request.args.get('date')
#     filtered_data = df[df['DateTime'] == date].to_dict(orient='records')
#     if not filtered_data:
#         return jsonify({'error': 'No data found for the given date'}), 404
#     return jsonify(filtered_data[0])

# Route to get data by DateTime
# @app.route('/data/<string:datetime>', methods=['GET'])
# def get_data_by_datetime(datetime):
#     row = df[df['DateTime'] == datetime]
#     if row.empty:
#         return jsonify({'error': 'DateTime not found'}), 404
#     return jsonify(row.to_dict(orient='records')[0])

# # Route to get angle differences for a specific planet
# @app.route('/data/angle/<string:planet1>/vs/<string:planet2>', methods=['GET'])
# def get_angle_difference(planet1, planet2):
#     column_name = f'{planet1} Position vs {planet2} Position'
#     if column_name not in df.columns:
#         return jsonify({'error': 'Invalid planet names'}), 404
#     data = df[['DateTime', column_name]].to_dict(orient='records')
#     return jsonify(data)



@app.route('/calculate-aspects', methods=['POST'])
def calculate_aspects():
    planet1 = request.json.get('planet1')
    planet2 = request.json.get('planet2')
    date_str = request.json.get('date')
    time_str = request.json.get('time')

    df1 = pd.read_csv(f'ephemeris/{planet1}.csv')
    df2 = pd.read_csv(f'ephemeris/{planet2}.csv')
    filtered_data1 = df1[(df1['date'] == date_str) & (df1['time'] == time_str)]
    filtered_data2 = df2[(df2['date'] == date_str) & (df2['time'] == time_str)]

    if len(filtered_data1) == 0 or len(filtered_data2) == 0:
        return jsonify({"error": "Data not available for both planets on the given date and time"}), 404

    position1= filtered_data1['absolute_position'].values[0]
    position2 = filtered_data2['absolute_position'].values[0]
    print(position1)
    print(position2)
    aspect = abs(position1 - position2)
    aspect_rev = (position2 - position1)

    return jsonify({
        "planet1": planet1,
        "planet2": planet2,
        "date": date_str,
        "time": time_str,
        "aspect": aspect,
        "aspect_rev": aspect_rev
    })












if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

