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
city='london'
# hours = get_planetary_hours(latitude, longitude, date)
hours = get_planetary_hours(city_position_obj[city], date)
# for start, end, planet in hours:
#     print(f"{start} - {end}: {planet}")


current_time = str(datetime.now().strftime("%H:%M"))
# current_time = datetime.strptime(str(current_time_1), "%H:%M").time()

print(type(current_time),'====')

# active_hour = highlight_active_hour(hours)


    # print(f"\nActive Planetary Hour:\n{active_hour}")
for start, end, planet in hours:
    start_time =str( datetime.strptime(start, "%H:%M").time())
    end_time = str(datetime.strptime(end, "%H:%M").time())
    # print(start_time,end_time, planet)
    if current_time > start_time and current_time < end_time:
        print(f"{start} - {end}: {planet} ---------- active")
    else:
        print(f"{start} - {end}: {planet} ")
    
    