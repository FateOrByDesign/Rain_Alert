import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo

# Used to load the .env data
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
        weather_data = {}
        city_and_country = get_owm_data(weather_data)
        print(city_and_country)
        print()
        # print the weather data
        for item in weather_data:
            print(f"{item} : {weather_data[item]}")
            print()
        # checks if it's going to rain
        message = check_if_rain(weather_data)
        # returns a msg to bring an umbrella or not
        send_alert_via_telegram(message)

def check_if_rain(weather_data: dict)->str:
    """Checks if it's going to rain and return a message to the user"""
    for item in weather_data:
        if weather_data[item][1] < 600:
            return "Bring An Umbrella!"
    return "Don't need a Umbrella run free!"

def calling_owm_api(api_end_point, params):
    """This calls the OWM API"""
    response = requests.get(api_end_point, params=params)
    response.raise_for_status()
    data = response.json()
    return data

def formated_data_time(data):
    """Given the data it calculates the local time in sri lanka from the unix dateandtime given"""
    timestamp = data["dt"]
    time_object = datetime.fromtimestamp(timestamp, tz=ZoneInfo("Asia/Colombo"))
    time = str(time_object).split("+")[0]
    return time

def get_starting_weather_data():
    """ Return the current weather from the CURRENT OWM API"""
    data = calling_owm_api(f"{OWM_API_ENDPOINT}weather", OWM_PARAMS)
    # format  the time accordingly
    time = formated_data_time(data)
    weather = data["weather"][0]
    return (time, weather["main"], weather["id"])


def get_owm_data(weather_data: dict) -> str:
    """ Get the weather data after the initial request by 3 hour intervals"""
    owm_params = OWM_PARAMS.copy()
    owm_params["cnt"] = "4"
    data = calling_owm_api(f"{OWM_API_ENDPOINT}forecast", owm_params)
    # get the starting time, condition and weather code on the first time the program ran
    time, condition, weather_code = get_starting_weather_data()
    # assign that to t weather_data dict
    weather_data[time] = (condition, weather_code)

    city_country = f"{data["city"]["name"]},{data["city"]["country"]}"

    # go through the list of weather by 3 hour context and add them to the weather_data dict
    data = data["list"]
    for weather_condition in data:
        time = formated_data_time(weather_condition)
        for weather in weather_condition["weather"]:
            weather_data[time] = (weather["main"], weather["id"])

    return city_country

    # if everything was successful then return the city name and country code


def send_alert_via_telegram(message):
    params = {
        "chat_id" : CHAT_ID,
        "text" : message,
    }
    response = requests.get(url=TELEGRAM_ENDPOINT, params=params)
    if response.status_code != 200:
        print("Couldn't Send message via Telegram")
        response.raise_for_status()
    else:
        print("Message was sent successfully.")


main()