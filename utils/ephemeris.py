import swisseph as swe
import datetime
import os
import pytz
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
path = os.getcwd()


def get_degree_minute_zodiac(pos):
    deg = int(pos)
    degree = deg % 30
    minute = (pos - deg) * 60
    zodiac = int(deg / 30) + 1
    return (degree, zodiac, minute)


def get_planet_position(planet):
    swe.set_ephe_path(f"{path}\swisseph")
    current_time = datetime.datetime.utcnow()
    planet_num = planet
    lat = 26.8467
    lon = 80.9462
    alt = 123

    # ================ JULIAN_TIME ====================================
    jday = swe.utc_to_jd(current_time.year, current_time.month,
                         current_time.day, current_time.hour,
                         current_time.minute, current_time.second, 1)
    swe.set_topo(lon, lat, alt)
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    planet_pos = swe.calc(jday[0], planet_num, swe.FLG_SIDEREAL)
    # print(house_pos[0][0])
    return (planet_pos[0][0])


def get_houses_position():
    swe.set_ephe_path(f"{path}\swisseph")

    local_tz = pytz.timezone('Asia/Kolkata')
    current = datetime.datetime.now(local_tz)
    UTCdt = swe.utc_time_zone(current.year, current.month, current.day,
                              current.hour, current.minute, current.second, 5.5)
    JD = swe.utc_to_jd(UTCdt[0], UTCdt[1], UTCdt[2],
                       UTCdt[3], UTCdt[4], 0, 1)
    natalUT = JD[1]
    # Ayanamsha
    ayanamsha = swe.get_ayanamsa(natalUT)
    # print('Lahiri Ayanamsha :', ayanamsha)
    LAT = 26.8467
    LON = 80.9462
    hsysP = bytes('E', 'utf-8')
    house_pos = swe.houses_ex(natalUT, LAT, LON, hsysP,
                              swe.FLG_SIDEREAL)

    # house_pos = swe.houses(natalUT, LAT, LON, hsysP)

    return [house_pos[0], ayanamsha]


def get_planet_by_date_time(planet):

    swe.set_ephe_path(f"{path}\swisseph")
    year = 1995
    month = 7
    day = 14
    hour =19
    minute = 58
    second = 0

    planet_num = planet
    lat = 26.85
    lon = 80.91
    alt = 123
    current = datetime.datetime(year, month, day, hour, minute, second)

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
