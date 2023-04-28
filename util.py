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
    hsysP = bytes('P', 'utf-8')
    house_pos = swe.houses_ex(natalUT, LAT, LON, hsysP,
                              swe.FLG_SIDEREAL)

    # house_pos = swe.houses(natalUT, LAT, LON, hsysP)

    return [house_pos[0], ayanamsha]


# def get_ingress_time():

#     # Set the path to the ephemeris file
#     swe.set_ephe_path(f"{path}\swisseph")

#     # Set the date and time
#     date = datetime.datetime(2023, 5, 1, 0, 0, 0)

#     # Calculate the Julian Day
#     jd = swe.utc_to_jd(date.year, date.month, date.day,
#                        date.hour, date.minute, date.second, 1)[1]

#     # Get the position of the Sun
#     sun_pos = swe.calc_ut(jd, swe.SUN)[0]

#     # Get the position of the Ascendant to determine the house cusps
#     asc_pos = swe.houses(jd, 0.0, 0.0)[1]

#     # Determine the house that the Sun is in
#     sun_house = None
#     for i in range(12):
#         if sun_pos >= asc_pos[i] and sun_pos < asc_pos[i+1]:
#             sun_house = i+1
#             break

#     # Determine the time when the Sun enters Taurus
#     if sun_house == 2:
#         ingress_time = date
#     else:
#         next_date = date + datetime.timedelta(days=1)
#         next_jd = swe.utc_to_jd(next_date.year, next_date.month, next_date.day,
#                                 next_date.hour, next_date.minute, next_date.second, 1)[1]
#         next_asc_pos = swe.houses(next_jd, 0.0, 0.0)[1]
#         if sun_pos < next_asc_pos[1]:
#             ingress_time = next_date
#         else:
#             ingress_time = date
#         return ingress_time


# print(get_ingress_time())
