
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



def get_degree_minute_zodiac(pos):
    deg = int(pos)
    degree = deg % 30
    minute = (pos - deg) * 60
    zodiac = int(deg / 30)
    return (degree, zodiacData[zodiac]['sign'], minute)


print(get_degree_minute_zodiac(58.0075))