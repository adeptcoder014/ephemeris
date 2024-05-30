import swisseph as swe
import datetime

def find_transit_date(planet, start_date, zodiac_sign):
    # Convert the start date to Julian Day
    jd = swe.julday(start_date.year, start_date.month, start_date.day)
    
    # Loop to find the date of the transit
    while True:
        # Calculate the position of the planet
        planet_pos = swe.calc_ut(jd, planet)[0]
        print('planet_pos', planet_pos)
        # Check if the planet has entered the desired zodiac sign
        if zodiac_sign * 30 <= planet_pos < (zodiac_sign + 1) * 30:
            break
        
        # Increment the Julian Day by 1 (one day at a time)
        jd += 1
    
    # Convert the Julian Day back to a Gregorian date
    transit_date = swe.revjul(jd)
    return datetime.date(transit_date[0], transit_date[1], transit_date[2])

# Define the planet and the zodiac sign (0 = Aries, 1 = Taurus, ..., 11 = Pisces)
planet = swe.SUN  # Example: SUN
zodiac_sign = 0  # Example: Aries

# Define the start date for the search
start_date = datetime.date(2024, 1, 1)

# Find the transit date
transit_date = find_transit_date(planet, start_date, zodiac_sign)
print(f"The {swe.get_planet_name(planet)} transits into {swe.get_sign_name(zodiac_sign)} on {transit_date}")
