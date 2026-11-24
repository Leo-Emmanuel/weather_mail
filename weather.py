import json
import urllib.request
from urllib.parse import urlencode


def search_locations(city):

    query_string = urlencode({
        "name": city,
        "count": 10,
        "language": "en",
        "format": "json"
    })

    url = "https://geocoding-api.open-meteo.com/v1/search?" + query_string

    response = urllib.request.urlopen(url)

    data = json.loads(response.read().decode("utf-8"))

    results = data.get("results", [])

    if not results:
        return []

    locations = []

    for location in results:
        locations.append({
            "name": location["name"],
            "country": location.get("country"),
            "admin1": location.get("admin1"),
            "latitude": location["latitude"],
            "longitude": location["longitude"]
        })

    return locations


def get_weather(latitude, longitude):

    query_string = urlencode({
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m",
        "timezone": "auto"
    })

    url = "https://api.open-meteo.com/v1/forecast?" + query_string

    response = urllib.request.urlopen(url)

    data = json.loads(response.read().decode("utf-8"))

    current = data["current"]

    weather = {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "feels_like": current["apparent_temperature"],
        "precipitation": current["precipitation"],
        "wind_speed": current["wind_speed_10m"]
    }

    return weather


def get_city_weather(location):

    latitude = location["latitude"]
    longitude = location["longitude"]

    weather = get_weather(latitude, longitude)

    return {
        "city": location["name"],
        "country": location.get("country"),
        "latitude": latitude,
        "longitude": longitude,
        "weather": weather
    }
