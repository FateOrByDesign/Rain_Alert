import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo
load_dotenv()

API_KEY = os.getenv("OWM_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")
TELEGRAM_ACCESS_TOKEN = os.getenv("TELEGRAM_ACCESS_TOKEN")
OWM_API_ENDPOINT = "https://api.openweathermap.org/data/2.5/"
TELEGRAM_ENDPOINT = f"https://api.telegram.org/bot{TELEGRAM_ACCESS_TOKEN}/sendMessage?"
OWM_PARAMS = {
        "lat": "6.84019",
        "lon": "79.87116",
        "appid": API_KEY,
        "units": "metric",
}

def main():
    if not API_KEY:
        print("Failed to load the .env!")
    else:
        message = get_owm_data()
        send_alert_via_telegram(message)

def get_starting_weather_date():
    response = requests.get(url=f"{OWM_API_ENDPOINT}/weather", params=OWM_PARAMS)
    response.raise_for_status()
    data = response.json()
    timestamp = data["dt"]
    time_object = datetime.fromtimestamp(timestamp, tz=ZoneInfo("Asia/Colombo"))
    time = str(time_object).split("+")[0]
    weather = data["weather"][0]
    return (time, weather["main"], weather["id"])


def get_owm_data():
    OWM_PARAMS["cnt"] = "5"
    response = requests.get(url=f"{OWM_API_ENDPOINT}forecast", params=OWM_PARAMS)
    response.raise_for_status()
    data = response.json()
    weather_data = {}
    weather_at_start = get_starting_weather_date()
    weather_data[weather_at_start[0]] = (weather_at_start[1], weather_at_start[2])

    print(f"{data["city"]["name"]},{data["city"]["country"]}")
    print()

    data = data["list"]
    for weather_condition in data:
        timestamp = weather_condition["dt"]
        time_object = datetime.fromtimestamp(timestamp, tz=ZoneInfo("Asia/Colombo"))
        time_object = str(time_object).split("+")[0]
        for weather in weather_condition["weather"]:
            weather_data[time_object] = (weather["main"], weather["id"])

    # print the day/time and the weather condition
    for item in weather_data:
        print(f"{item} : {weather_data[item]}")
        print()

    for item in weather_data:
        if weather_data[item][1] < 600:
            return "Bring An Umbrella!"

def send_alert_via_telegram(message):
    params = {
        "chat_id" : CHAT_ID,
        "text" : message,
    }
    response = requests.get(url=TELEGRAM_ENDPOINT, params=params)
    response.raise_for_status()
    if response.status_code != 200:
        print("Couldn't Send message via Telegram")
    else:
        print("Message was sent successfully.")

main()