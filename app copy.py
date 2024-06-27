from flask import Flask, request
import swisseph as swe
from datetime import datetime, timedelta

app = Flask(__name__)

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

def get_planet_by_date_time(planet, date, time):
    datetime_str = date + ' ' + time
    utc_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
    jd = swe.julday(utc_time.year, utc_time.month, utc_time.day, 
                    utc_time.hour + utc_time.minute / 60.0)
    return swe.calc_ut(jd, planet)

def get_degree_minute_zodiac(planet_pos):
    degree = planet_pos[0] % 360  # Extract degree from the tuple and apply modulo 360
    minute = (degree - int(degree)) * 60
    zodiac = int(degree // 30)
    return degree, zodiac, minute


@app.route('/get-planet-byDateTime_d', methods=['POST'])
def get_planet_byDateTime_d():
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    time = request.json['time']
    planet = request.json['planet']
    
    def handle_planet_swiss_value_from_name(planet_name):
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
        if planet_name in planet_swiss_value_obj:
            return planet_swiss_value_obj[planet_name]
        else:
            return f"Error: {planet_name} is not a valid planet."

    planet_swiss_value = handle_planet_swiss_value_from_name(planet)
    if isinstance(planet_swiss_value, str):
        return {"status": 400, "error": planet_swiss_value}

    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    current_datetime = start_datetime

    transit_data = []

    while current_datetime <= end_datetime:
        date_str = current_datetime.strftime('%Y-%m-%d')
        planet_pos = get_planet_by_date_time(planet_swiss_value, date_str, time)
        degree, zodiac, minute = get_degree_minute_zodiac(planet_pos)
        specificPlanetPositionForGivenDateTime = {
            'date': date_str,
            'name': planet,
            'position': {
                'degree': degree,
                'minute': minute,
                'sign': zodiacData[zodiac]['sign'],
                'name': zodiacData[zodiac]['name']
            }
        }
        transit_data.append(specificPlanetPositionForGivenDateTime)
        current_datetime += timedelta(days=1)

    return {
        "status": 200,
        "data": transit_data
    }

if __name__ == '__main__':
    app.run(debug=True)
