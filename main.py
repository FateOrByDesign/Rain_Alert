import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OWM_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")
TELEGRAM_ACCESS_TOKEN = os.getenv("TELEGRAM_ACCESS_TOKEN")
OWM_API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
TELEGRAM_ENDPOINT = f"https://api.telegram.org/bot{TELEGRAM_ACCESS_TOKEN}/sendMessage?"

def main():
    if not API_KEY:
        print("Failed to load the .env!")
    else:
        message = get_owm_data()
        send_alert_via_telegram(message)



def get_owm_data():
    params = {
        "lat": "6.84019",
        "lon": "79.87116",
        "appid": API_KEY,
        "units": "metric",
        "cnt": 4,
    }

    response = requests.get(OWM_API_ENDPOINT, params=params)
    response.raise_for_status()
    data = response.json()
    weather_data = {}

    print(f"{data["city"]["name"]},{data["city"]["country"]}")
    print()

    data = data["list"]
    for weather_condition in data:
        for weather in weather_condition["weather"]:
            weather_data[weather_condition["dt_txt"]] = (weather["main"], weather["id"])

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