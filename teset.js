const moment = require('moment-timezone');
const SunCalc = require('suncalc');

// Order of the planets in Chaldean sequence
const planets = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"];

// Mapping of days to ruling planets
const dayRuler = {
    0: "Moon",     // Monday
    1: "Mars",     // Tuesday
    2: "Mercury",  // Wednesday
    3: "Jupiter",  // Thursday
    4: "Venus",    // Friday
    5: "Saturn",   // Saturday
    6: "Sun"       // Sunday
};

function mins2hoursandmins(time) {
    const hours = Math.floor(time / 60);
    const minutes = time % 60;
    return `${hours}:${minutes < 10 ? '0' + minutes : minutes}`;
}

function getminutes4subtracting(start_time) {
    let minutes = parseInt(start_time.slice(-2));
    minutes -= 1;
    return minutes < 10 ? `0${minutes}` : `${minutes}`;
}

function gethours(time) {
    return Math.floor(time / 60).toString();
}

function getPlanetaryHours(city, date) {
    // Calculate sunrise and sunset times
    const { latitude, longitude, timezone } = city;
    const s = SunCalc.getTimes(date.toDate(), latitude, longitude);
    const timezoneObj = moment.tz.zone(timezone);
    const sunrise = moment.tz(s.sunrise, timezone);
    const sunset = moment.tz(s.sunset, timezone);

    // Length of day and night in hours
    const sunriseTotalMinutes = sunrise.hour() * 60 + sunrise.minute();
    const sunsetTotalMinutes = sunset.hour() * 60 + sunset.minute();
    const difference = sunsetTotalMinutes - sunriseTotalMinutes;
    const lengthOfHour = difference / 12;

    // Determine order of the planets based on Chaldean sequence
    const dayOfWeek = date.day();
    let chaldean = planets.slice();

    if (dayOfWeek === 0) {
        chaldean = ["Moon", "Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury"];
    } else if (dayOfWeek === 1) {
        chaldean = ["Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter"];
    } else if (dayOfWeek === 2) {
        chaldean = ["Mercury", "Moon", "Saturn", "Jupiter", "Mars", "Sun", "Venus"];
    } else if (dayOfWeek === 3) {
        chaldean = ["Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn"];
    } else if (dayOfWeek === 4) {
        chaldean = ["Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars", "Sun"];
    } else if (dayOfWeek === 5) {
        chaldean = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"];
    } else if (dayOfWeek === 6) {
        chaldean = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"];
    }

    // Repeat the sequence
    const newChaldean = chaldean.slice();
    chaldean = chaldean.concat(newChaldean).slice(0, -2);

    // Calculate end of hour and planetary hours
    const planetaryHours = [];
    for (let i = 0; i < 12; i++) {
        let startMinutes = sunriseTotalMinutes + i * lengthOfHour;
        let endMinutes = sunriseTotalMinutes + (i + 1) * lengthOfHour;
        
        let start = mins2hoursandmins(startMinutes);
        let end = mins2hoursandmins(endMinutes);
        let planet = chaldean[i % 7];

        planetaryHours.push({ start, end, planet });
    }

    return planetaryHours;
}

// Example usage
const cities = {
    london: {
        latitude: 51.5074,
        longitude: -0.1278,
        timezone: 'Europe/London'
    },
    delhi: {
        latitude: 28.7041,
        longitude: 77.1025,
        timezone: 'Asia/Kolkata'
    },
    mumbai: {
        latitude: 19.0760,
        longitude: 72.8777,
        timezone: 'Asia/Kolkata'
    },
    lucknow: {
        latitude: 26.8467,
        longitude: 80.9462,
        timezone: 'Asia/Kolkata'
    }
};

const date = moment('2034-07-04').subtract(1, 'days');
const city = 'london';  // Replace with the city you want to use
const hours = getPlanetaryHours(cities[city], date);
hours.forEach(({ start, end, planet }) => {
    console.log(`${start} - ${end}: ${planet}`);
});
