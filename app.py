from flask import Flask
import swisseph as swe
from util import get_planet_position, get_degree_minute_zodiac, zodiacData
# ==============================================================================

app = Flask(__name__)

# ==============================================================================


@app.route('/')
def get():
    sun = swe.SUN
    moon = swe.MOON
    mercury = swe.MERCURY
    venus = swe.VENUS
    mars = swe.MARS
    jupiter = swe.JUPITER
    saturn = swe.SATURN
    sun_pos = get_planet_position(sun)
    moon_pos = get_planet_position(moon)
    mercury_pos = get_planet_position(mercury)
    venus_pos = get_planet_position(venus)
    mars_pos = get_planet_position(mars)
    jupiter_pos = get_planet_position(jupiter)
    saturn_pos = get_planet_position(saturn)

    degree, zodiac, minute = get_degree_minute_zodiac(sun_pos)
    degree1, zodiac1, minute1 = get_degree_minute_zodiac(moon_pos)
    degree2, zodiac2, minute2 = get_degree_minute_zodiac(mercury_pos)
    degree3, zodiac3, minute3 = get_degree_minute_zodiac(venus_pos)
    degree4, zodiac4, minute4 = get_degree_minute_zodiac(mars_pos)
    degree5, zodiac5, minute5 = get_degree_minute_zodiac(jupiter_pos)
    degree6, zodiac6, minute6 = get_degree_minute_zodiac(saturn_pos)

    message = {
        "☀": f"{degree} degree {round(minute)} minute in {zodiacData[zodiac]}",
        "🌙": f"{degree1} degree {round(minute1)} minute in {zodiacData[zodiac1]}",
        "☿️": f"{degree2} degree {round(minute2)} minute in {zodiacData[zodiac2]}",
        "♀️": f"{degree3} degree {round(minute3)} minute in {zodiacData[zodiac3]}",
        "♂️": f"{degree4} degree {round(minute4)} minute in {zodiacData[zodiac4]}",
        "♃": f"{degree5} degree {round(minute5)} minute in {zodiacData[zodiac5]}",
        "♄": f"{degree6} degree {round(minute6)} minute in {zodiacData[zodiac6]}",

    }

    json = {
        "status": 200,
        "data": message
    }
    return json
# ==============================================================================


if __name__ == '__main__':
    app.run()
