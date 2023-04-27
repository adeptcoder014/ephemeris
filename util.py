import swisseph as swe
import datetime

zodiacData = {
    1: '♈',
    2: '♉',
    3: '♊',
    4: '♋',
    5: '♌',
    6: '♍',
    7: '♎',
    8: '♏',
    9: '♐',
    10: '♑',
    11: '♒',
    12: '♓ ',
}

# =============================================

def get_planet_position():
    swe.set_ephe_path("C:/Users/NISCHAL/Desktop/cerridwen/swisseph")
    td = swe.date_conversion(2023, 4, 26, 11.41)
    pos = swe.calc(2460060.975416667, 4)
    print("=============================", pos)


def get_degree_minute_zodiac(pos):
    deg = int(pos)

    degree = deg % 30
    minute = (pos - deg) * 60
    zodiac = int(deg / 30) + 1
    return (degree, zodiac, minute)


def get_planet_position(planet):
    swe.set_ephe_path("C:/Users/NISCHAL/Desktop/ephemeris/swisseph")
    current_time = datetime.datetime.utcnow()
    time_ist = datetime.datetime.now()
    planet_num = planet
    lat = 26.8467
    lon = 80.9462
    alt = 123
  

    # ================ JULIAN_TIME ====================================
    jday = swe.utc_to_jd(current_time.year, current_time.month,
                         current_time.day, current_time.hour,
                         current_time.minute, current_time.second, 1)
    house_pos = swe.houses(
        jday[0],
        lat,
        lon,
    )
    swe.set_topo(lon, lat, alt)
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    planet_pos = swe.calc(jday[0], planet_num, swe.FLG_SIDEREAL)
    # print(house_pos[0][0])
    return (planet_pos[0][0])
