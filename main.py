import os

import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = os.getenv("OWM_API_KEY")

if not API_KEY:
    print("Failed to load the .env!")
else:
    params = {
        "lat" : "6.84019",
        "lon" : "79.87116",
        "appid" : API_KEY,
        "units" : "metric",
        "cnt" : 4,
    }

    response = requests.get(API_ENDPOINT, params=params)
    response.raise_for_status()
    data = response.json()
    weather_data = {}

    print(f"{data["city"]["name"]},{data["city"]["country"]}")
    print()

    data = data["list"]
    for weather_condition in data:
        for weather in weather_condition["weather"]:
            weather_data[weather_condition["dt_txt"]] = weather["main"]

    for item in weather_data:
        print(f"{item} : {weather_data[item]}")
        print()

    now = datetime.now()
    now = str(now).split()[1].split(".")[0]