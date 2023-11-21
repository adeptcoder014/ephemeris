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

# ==============================================================================


# @app.route('/')
# def get():
#     sun = swe.SUN
#     moon = swe.MOON
#     mercury = swe.MERCURY
#     venus = swe.VENUS
#     mars = swe.MARS
#     jupiter = swe.JUPITER
#     saturn = swe.SATURN
#     sun_pos = get_planet_position(sun)
#     moon_pos = get_planet_position(moon)
#     mercury_pos = get_planet_position(mercury)
#     venus_pos = get_planet_position(venus)
#     mars_pos = get_planet_position(mars)
#     jupiter_pos = get_planet_position(jupiter)
#     saturn_pos = get_planet_position(saturn)

#     degree, zodiac, minute = get_degree_minute_zodiac(sun_pos)
#     degree1, zodiac1, minute1 = get_degree_minute_zodiac(moon_pos)
#     degree2, zodiac2, minute2 = get_degree_minute_zodiac(mercury_pos)
#     degree3, zodiac3, minute3 = get_degree_minute_zodiac(venus_pos)
#     degree4, zodiac4, minute4 = get_degree_minute_zodiac(mars_pos)
#     degree5, zodiac5, minute5 = get_degree_minute_zodiac(jupiter_pos)
#     degree6, zodiac6, minute6 = get_degree_minute_zodiac(saturn_pos)

#     message = [
#         {
#             'name': "sun",
#             'position': f"{degree} degree {round(minute)} minute in {zodiacData[zodiac]}"
#         },
#         {
#             'name': "moon",
#             'position': f"{degree1} degree {round(minute1)} minute in {zodiacData[zodiac1]}",
#         },
#         {
#             'name': "mercury",
#             'position': f"{degree2} degree {round(minute2)} minute in {zodiacData[zodiac2]}",
#         },
#         {
#             'name': "venus",
#             'position': f"{degree3} degree {round(minute3)} minute in {zodiacData[zodiac3]}",
#         },
#         {
#             'name': "mars",
#             'position': f"{degree4} degree {round(minute4)} minute in {zodiacData[zodiac4]}",
#         },
#         {
#             'name': "jupiter",
#             'position': f"{degree5} degree {round(minute5)} minute in {zodiacData[zodiac5]}",
#         },
#         {
#             'name': "saturn",
#             'position':  f"{degree6} degree {round(minute6)} minute in {zodiacData[zodiac6]}",
#         },
#     ]

#     json = {
#         "status": 200,
#         "data": message
#     }
#     return json

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
    # message=[
    #     {
    #         'name': swe.get_planet_name(planet),
    #         'position': f"{degree}° {zodiacData[zodiac]} {round(minute)}'"
    #     }
    #     for planet in planets
    #     planet_pos = get_planet_position(planet,lat, long, date, timeOfBirth)
    #     degree,zodiac, minute = get_degree_minute_zodiac(planet_pos)
    #     ]
    for planet in planets:
        planet_pos = get_planet_position(planet, lat, long, date, timeOfBirth)
        degree, zodiac, minute = get_degree_minute_zodiac(planet_pos)
        # message.append({
        #     'name': swe.get_planet_name(planet),
        #     'position': f"{degree}° {zodiacData[zodiac]} {round(minute)}'"
        # })

        message.append({
            'name': swe.get_planet_name(planet).lower(),
            # 'position': f"{degree}° {zodiacData[zodiac]} {round(minute)}'",
            'position': {
                'degree': degree,
                "minute": minute,
                'sign': zodiacData[zodiac]['sign'],
                'name': zodiacData[zodiac]['name']
            }
        })

    print('---------------------- message -------------------------------', message)
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






@app.route('/get-planet-byDateTime', methods=['GET'])
def get_planet_byDateTime():
    dateTime = request.json['date']
    
   
    dataP= getPlanetsByDate(dateTime)
    print(f"---  dataP -----",  dataP)
    return

    # planets = [
    #     swe.MOON,
    #     swe.MERCURY,
    #     swe.VENUS,
    #     swe.SUN,
    #     swe.MARS,
    #     swe.JUPITER,
    #     swe.SATURN,
    #     swe.MEAN_NODE]
    # message = []

    

    print('---------------------- message -------------------------------', message)
    return {
        "status": 200,
        "data": "message"
    }


if __name__ == '__main__':
    app.run()
