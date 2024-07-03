from flask import Flask, request
import swisseph as swe
from datetime import datetime, timedelta
import os
from time import sleep
import json

app = Flask(__name__)
path = os.getcwd()

zodiacData = {
    0: {'name': 'aries', 'sign': '♈'},
    1: {'name': 'taurus', 'sign': '♉'},
    2: {'name': 'gemini', 'sign': '♊'},
    3: {'name': 'cancer', 'sign': '♋'},
    4: {'name': 'leo', 'sign': '♌'},
    5: {'name': 'virgo', 'sign': '♍'},
    6: {'name': 'libra', 'sign': '♎'},
    7: {'name': 'scorpio', 'sign': '♏'},
    8: {'name': 'sagittarius', 'sign': '♐'},
    9: {'name': 'capricorn', 'sign': '♑'},
    10: {'name': 'aquarius', 'sign': '♒'},
    11: {'name': 'pisces', 'sign': '♓'}
}

angles = [0.00, 11.25, 30.00, 60.00, 90.00, 120.00, 150.00, 180.00, 210.00, 240.00, 270.00, 300.00, 330.00]

def get_planet_by_date_time(planet, date, time):
    swe.set_ephe_path(f"{path}/swisseph")
    year = int(date.split("-")[0])
    month = int(date.split("-")[1])
    day = int(date.split("-")[2])
    hour = int(time.split(":")[0])
    minute = int(time.split(":")[1])
    second = 0

    current = datetime(year, month, day, hour, minute, second)
    UTCdt = swe.utc_time_zone(current.year, current.month, current.day,
                              current.hour, current.minute, current.second, 5.5)
    jday = swe.utc_to_jd(UTCdt[0], UTCdt[1],
                         UTCdt[2], UTCdt[3],
                         UTCdt[4], UTCdt[5], 1)
    swe.set_topo(80.92, 26.84, 123)  # Lon, Lat, Alt
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    planet_pos = swe.calc(jday[0], planet, swe.FLG_SIDEREAL)
    return planet_pos[0]  # Return degree

def get_degree_minute_zodiac(planet_pos):
    deg = int(planet_pos)
    degree = deg % 30
    minute = (planet_pos - deg) * 60
    zodiac = int(deg / 30)
    return degree, zodiac, minute

@app.route('/get-planet-byDateTime_d', methods=['POST'])
def get_planet_byDateTime_d():
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    time = request.json['time']
    planet = request.json['planet']
    
    planet_swiss_value_obj = {
        'venus': swe.VENUS,
        'moon': swe.MOON,
        'mercury': swe.MERCURY,
        'sun': swe.SUN,
        'mars': swe.MARS,
        'jupiter': swe.JUPITER,
        'saturn': swe.SATURN,
        'meanNode': swe.MEAN_NODE
    }
    planet_swiss_value = planet_swiss_value_obj.get(planet)
    if planet_swiss_value is None:
        return {"status": 400, "error": "Invalid planet name"}

    start_datetime = datetime.strptime(start_date + ' ' + time, '%Y-%m-%d %H:%M')
    end_datetime = datetime.strptime(end_date + ' ' + time, '%Y-%m-%d %H:%M')
    current_datetime = start_datetime

    transit_data = []
    angle_index = 0

    while current_datetime <= end_datetime :
    # while current_datetime <= end_datetime and angle_index < len(angles):
        date_str = current_datetime.strftime('%Y-%m-%d')
        time_str = current_datetime.strftime('%H:%M')
        
        planet_pos = get_planet_by_date_time(planet_swiss_value, date_str, time_str)
        # print(date_str,time_str,round(planet_pos[0], 2) )
        # print('------',len(angles) ,angle_index,angles[angle_index])
        print('=============================', round(planet_pos[0], 1))
        if round(planet_pos[0], 1) == angles[angle_index]:
            print('=======  ofund  ======================' )
            degree, zodiac, minute = get_degree_minute_zodiac(round(planet_pos[0], 2))
            
            specificPlanetPositionForGivenDateTime = {
                'name': planet,
                'date': current_datetime.strftime('%Y-%m-%d'),
                'time': current_datetime.strftime('%H:%M:%S'),           
                'position': {
                    'degree': degree,
                    'minute': round(minute),
                    # 'sign': zodiacData[zodiac]['sign'],
                    'name': zodiacData[zodiac]['name']
                }
            }
            transit_data.append(specificPlanetPositionForGivenDateTime)

        angle_index += 1  # Move to the next angle
        if angle_index == len(angles) :
                angle_index=0
        
        
        current_datetime += timedelta(minutes=1)  # Iterate minute by minute

    with open('transit_data.json', 'w') as json_file:
        json.dump(transit_data, json_file, indent=4, ensure_ascii=False)

    return {
        "status": 200,
        "data": transit_data
    }

if __name__ == '__main__':
    app.run()
