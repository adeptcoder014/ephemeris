from flask import Flask, request
import swisseph as swe
import requests
from util import get_planet_position, get_degree_minute_zodiac, get_moon_position, zodiacData, get_houses_position, get_planet_by_date_time,getPlanetsByDate

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
    data = request.json['value']
    lat = data['location']['lat']
    long = data['location']['long']
    date = data['dob']
    timeOfBirth = data['time']

    data['location']
    positions = get_houses_position(lat, long, date, timeOfBirth)[0]
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





if __name__ == '__main__':
    app.run()
