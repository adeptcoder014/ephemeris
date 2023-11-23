from flask import Flask, request
import swisseph as swe
import requests
from util import get_planet_position, get_degree_minute_zodiac, get_moon_position, zodiacData, get_houses_position, get_planet_by_dateTime,getPlanetsByDate

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


@app.route('/natal', methods=['GET', 'POST'])
def get_natal():
    planets = [swe.SATURN, swe.JUPITER, swe.MARS,
               swe.SUN, swe.VENUS,  swe.MERCURY, swe.MOON]
    message = []

    for planet in planets:
        planet_pos = get_planet_by_dateTime(planet)
        degree, zodiac, minute = get_degree_minute_zodiac(planet_pos)
        message.append({
            'name': swe.get_planet_name(planet),
            'position': f"{degree}° {zodiacData[zodiac]} {round(minute)}'"
        })

    return {
        "status": 200,
        "data": message,
    }
# ===================================================================


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






@app.route('/get-planet-byDateTime', methods=['POST'])
def get_planet_byDateTime():
    date = request.json['date']

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

    print("zodiacData-----",zodiacData)
    for planet in planets:
        planet_pos = get_planet_by_dateTime(planet)
        degree, zodiac, minute = get_degree_minute_zodiac(planet_pos)

        planetPositionForGivenDateTime.append({
            'name': swe.get_planet_name(planet).lower(),
            'position': {
                'degree': degree,
                "minute": minute,
                'sign': zodiacData[zodiac]['sign'],
                # 'name': zodiacData[zodiac]['name']
            }
        })   

    
   
    # dataP= getPlanetsByDate(date)

    return {
        "status": 200,
        "data": planetPositionForGivenDateTime
    }


if __name__ == '__main__':
    app.run()
