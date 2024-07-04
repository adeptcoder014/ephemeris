import swisseph as swe
import datetime
from datetime import time

import os
import pytz
# zodiacData = {
#     1: '♈',
#     2: '♉',
#     3: '♊',
#     4: '♋',
#     5: '♌',
#     6: '♍',
#     7: '♎',
#     8: '♏',
#     9: '♐',
#     10: '♑',
#     11: '♒',
#     12: '♓ ',
# }

zodiacData = [
    {
        "serial": 1,
        "sign": "♈",
        "name": "aries"
    },
     {
        "serial": 2,
        "sign": "♉",
        "name": "taurus"
    },
     {
        "serial": 3,
        "sign": "♊",
        "name": "gemini"
    },
     {
        "serial": 4,
        "sign": "♋",
        "name": "cancer"
    },
     {
        "serial": 5,
        "sign": "♌",
        "name": "leo"
    },
     {
        "serial": 6,
        "sign": "♍",
        "name": "virgo"
    },
     {
        "serial": 7,
        "sign": "♎",
        "name": "libra"
    },
     {
        "serial": 8,
        "sign": "♏",
        "name": "scorpio"
    },
     {
        "serial": 9,
        "sign": "♐",
        "name": "sagittarius"
    },
     {
        "serial": 10,
        "sign": "♑",
        "name": "capricorn"
    },
     {
        "serial": 11,
        "sign": "♒",
        "name": "aquarius"
    },
     {
        "serial": 12,
        "sign": "♓",
        "name": "pisces"
    }
]


# =============================================
path = os.getcwd()


def get_degree_minute_zodiac(pos):
    deg = int(pos)
    degree = deg % 30
    minute = (pos - deg) * 60
    zodiac = int(deg / 30)
    return (degree, zodiac, minute)


def get_planet_position(planet, lat, long, date, timeOfBirth):
    swe.set_ephe_path(f"{path}\swisseph")

    current_time = datetime.datetime.utcnow()
    planet_num = planet
    lat = lat
    long = long
    # alt = 123
    incomingYear = date.split("-")[0]
    incomingMonth = date.split("-")[1]
    incomingDay = date.split("-")[2]
    incomingHour = timeOfBirth.split(":")[0]
    incomingMinute = timeOfBirth.split(":")[1]

    date_string = date
    date_format = "%Y-%m-%d"

    date_object = datetime.datetime.strptime(date_string, date_format)

    local_time = datetime.datetime.combine(
        date_object, time(int(incomingHour), int(incomingMinute)))

    local_timezone = pytz.timezone('Asia/Kolkata')
    utc_time = local_timezone.localize(local_time).astimezone(pytz.UTC)

    # ================ JULIAN_TIME ====================================
    # jday = swe.utc_to_jd(current_time.year, current_time.month,
    #                      current_time.day, current_time.hour,
    #                      current_time.minute, current_time.second, 1)
    jday_new = swe.utc_to_jd(int(incomingYear), int(incomingMonth), int(incomingDay),
                             utc_time.hour, utc_time.minute, 0, 1)
    swe.set_topo(long, lat)
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    planet_pos = swe.calc(jday_new[0], planet_num, swe.FLG_SIDEREAL)
    return (planet_pos[0][0])


def get_houses_position(lat, long, date, time):
    swe.set_ephe_path(f"{path}\swisseph")

    local_tz = pytz.timezone('Asia/Kolkata')
    current = datetime.datetime.now(local_tz)

    incomingYear = date.split("-")[0]
    incomingMonth = date.split("-")[1]
    incomingDay = date.split("-")[2]
    incomingHour = time.split(":")[0]
    incomingMinute = time.split(":")[1]

    # UTCdt = swe.utc_time_zone(current.year, current.month, current.day,
    #                           current.hour, current.minute, current.second, 5.5)

    UTCdt_new = swe.utc_time_zone(int(incomingYear), int(incomingMonth), int(incomingDay),
                                  int(incomingHour), int(incomingMinute), 0, 5.5)

    JD = swe.utc_to_jd(UTCdt_new[0], UTCdt_new[1], UTCdt_new[2],UTCdt_new[3], UTCdt_new[4], 0, 1)

    natalUT = JD[1]
    ayanamsha = swe.get_ayanamsa(natalUT)
    LAT = lat
    LON = long
    hsysP = bytes('E', 'utf-8')
    house_pos = swe.houses_ex(natalUT, LAT, LON, hsysP,swe.FLG_SIDEREAL)

    return [house_pos[0], ayanamsha]


def get_planet_by_date_time(planet,date,time):


    swe.set_ephe_path(f"{path}\swisseph")
    year = int(date.split("-")[0])
    month = int(date.split("-")[1])
    day = int(date.split("-")[2])
    hour = int(time.split(":")[0])
    minute = int(time.split(":")[1])
    second = 00

    planet_num = planet
    lat = 26.85
    lon = 80.91
    alt = 123
    current = datetime(year, month, day, hour, minute, second)

    UTCdt = swe.utc_time_zone(current.year, current.month, current.day,
                              current.hour, current.minute, current.second, 5.5)
    # ================ JULIAN_TIME ====================================
    jday = swe.utc_to_jd(UTCdt[0], UTCdt[1],
                         UTCdt[2], UTCdt[3],
                         UTCdt[4], UTCdt[5], 1)
    swe.set_topo(lon, lat, alt)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    planet_pos = swe.calc(jday[0], planet_num, swe.FLG_SIDEREAL)
    # print(house_pos[0][0])
    return (planet_pos[0][0])


def get_moon_position():
    swe.set_ephe_path(f"{path}\swisseph")
    current_time = datetime.datetime.utcnow()
    planet_num = swe.MOON
    lat = 26.8467
    lon = 80.9462
    # alt = 123

    # ================ JULIAN_TIME ====================================
    jday = swe.utc_to_jd(current_time.year, current_time.month,
                         current_time.day, current_time.hour,
                         current_time.minute, current_time.second, 1)

    swe.set_topo(lon, lat)
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    planet_pos = swe.calc(jday[0], planet_num, swe.FLG_SIDEREAL)
    # print(house_pos[0][0])
    return (planet_pos[0][0])



def getPlanetsByDate(dateTime):
    swe.set_ephe_path(f"{path}\swisseph")

    current_time = dateTime.datetime.utcnow()
    planet_num = swe.MOON
    lat = 26.8467
    long = 80.9462
    # alt = 123
    incomingYear = date.split("-")[0]
    incomingMonth = date.split("-")[1]
    incomingDay = date.split("-")[2]
    # incomingHour = timeOfBirth.split(":")[0]
    # incomingMinute = timeOfBirth.split(":")[1]

    date_string = date
    date_format = "%Y-%m-%d"

    date_object = datetime.datetime.strptime(date_string, date_format)

    # local_time = datetime.datetime.combine(
    #     date_object, time(int(incomingHour), int(incomingMinute)))
    local_time = datetime.datetime.combine(date_object)


    local_timezone = pytz.timezone('Asia/Kolkata')
    utc_time = local_timezone.localize(local_time).astimezone(pytz.UTC)

    # ================ JULIAN_TIME ====================================
    # jday = swe.utc_to_jd(current_time.year, current_time.month,
    #                      current_time.day, current_time.hour,
    #                      current_time.minute, current_time.second, 1)
    jday_new = swe.utc_to_jd(int(incomingYear), int(incomingMonth), int(incomingDay),
                             utc_time.hour, utc_time.minute, 0, 1)
    swe.set_topo(long, lat)
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    planet_pos = swe.calc(jday_new[0], planet_num, swe.FLG_SIDEREAL)
    return (planet_pos[0][0])
 
 
 
# =========================================================
# =-================ Planetary hours =======================
from datetime import datetime, timedelta
from astral.sun import sun
from astral import LocationInfo
import pytz

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
    location = LocationInfo(city['astral_value'][0],city['astral_value'][1],city['astral_value'][2] ,city['latitude'], city['longitude'])
    
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

# Example usage

city_position_obj={
    'london' : {
        'latitude' : 51.5074,  
        'longitude' : -0.1278  ,
        'astral_value':("London", "England", "Europe/London")
    },
     'delhi' : {
        'latitude' : 28.7041,  
        'longitude' : 77.1025,
        'astral_value':("Delhi", "India", "Asia/Kolkata")
    },
      'mumbai' : {
        'latitude' : 19.0760,  
        'longitude' : 72.8777 ,
        'astral_value':("Mumbai", "India", "Asia/Kolkata")
    },
       'lucknow' : {
        'latitude' : 26.8467,  
        'longitude' : 80.9462  ,
        'astral_value':("Lucknow", "India", "Asia/Kolkata")
    }
}
        
date = datetime(2024, 7, 4)
# latitude = 51.5074  # Latitude of London
# longitude = -0.1278  # Longitude of London
city='mumbai'
# hours = get_planetary_hours(latitude, longitude, date)
hours = get_planetary_hours(city_position_obj[city], date)
for start, end, planet in hours:
    print(f"{start} - {end}: {planet}")



# =========================================================
# =========================================================