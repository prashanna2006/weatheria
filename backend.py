import flet as ft
import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

load_dotenv()
key = os.getenv('API_KEY')

# gui_values = {
#         "search_bar": search_bar.content.value,
#         "city_name": city_container.content.value,
#         "current_temp": current_temp_container.content.value,
#         "max_temp": max_temp_container.content.value,
#         "min_temp": min_temp_container.content.value,
#         "weather_desc": weather_desc_container.content.value,
#         "feels_like": feels_like_container.content.value,
#         "sunrise": sunrise_stack.controls[2].content.value,
#         "sunset": sunset_stack.controls[2].content.value,
#         "wind_speed": wind_stack.content.controls[2].content.value,
#         "humidity": humidity_stack.content.controls[2].content.value,
#         "pressure": pressure_stack.content.controls[2].content.value,
#         "visibility": visibility_stack.content.controls[2].content.value,
#         "sea_lvl": sea_lvl_stack.content.controls[2].content.value,
#         "ground_lvl": ground_lvl_stack.content.controls[2].content.value,
#         "error": error_container.content.value,
#     }

# api_values = [
#                 data["name"], data["main"]["temp"], data["main"]["temp_max"], data["main"]["temp_min"], data["weather"][0]["description"], data["main"]["feels_like"],
#                 data["sys"]["sunrise"], data["sys"]["sunset"], data["wind"]["speed"], data["main"]["humidity"], data["main"]["pressure"], data["visibility"],
#                 data["main"]["sea_level"], data["main"]["grnd_level"], data["sys"]["country"]
#                 ]

# def error_display(error, gui_values):
#     gui_values["error"].value = error
#     gui_values["error"].color = ft.Colors.RED_600
#     gui_values["error"].update()


def timezone_convert(timestamp, timezone_offset):
    utc_time = datetime.fromtimestamp(timestamp, tz = timezone.utc)
    local_time = utc_time + timedelta(seconds = timezone_offset)
    return local_time.strftime('%I:%M %p')


def display_weather(data, gui_values, timezone):
    gui_values["city_name"].value = f'{data["name"]}, {data["sys"]["country"]}'
    gui_values["current_temp"].value = f"{round(int(data["main"]["temp"]))}\u00B0F"
    gui_values["max_temp"].value = f"{round(int(data["main"]["temp_max"]))}\u00B0F"
    gui_values["min_temp"].value = f"{round(int(data["main"]["temp_min"]))}\u00B0F"
    gui_values["weather_desc"].value = f'{data["weather"][0]["description"]}'.title()
    gui_values["feels_like"].value = f'Feels like: {data["main"]["feels_like"]}\u00B0F'
    gui_values["sunrise"].value = timezone_convert(data["sys"]["sunrise"], timezone)
    gui_values["sunset"].value = timezone_convert(data["sys"]["sunset"], timezone)
    gui_values["wind_speed"].value = f'{data["wind"]["speed"]} km/hr'
    gui_values["humidity"].value = f'{data["main"]["humidity"]} %'
    gui_values["pressure"].value = f'{data["main"]["pressure"]} hPa'
    gui_values["visibility"].value = f'{data["visibility"]} m'
    gui_values["sea_lvl"].value = f'{data["main"]["sea_level"]} m'
    gui_values["ground_lvl"].value = f'{data["main"]["grnd_level"]} m'

    for value in gui_values.values():
        if hasattr(value, "update"):
            value.update()
    gui_values["search_bar"].value = None
    gui_values["search_bar"].update()
    gui_values["error"].value = None
    gui_values["error"].update()


def get_weather(gui_values):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={gui_values["search_bar"].value}&appid={key}&units=imperial"
        response = requests.get(url)
        response.raise_for_status() # Raises exception for HTTP errors
        data = response.json()
        print(data)
        if data["cod"] == 200:
            display_weather(data, gui_values, data["timezone"])
            
    
    except requests.exceptions.HTTPError as http_error:
        status_code = response.status_code
        match status_code:
            case 400:
                if gui_values["search_bar"].value != "":
                    print("Bad Request: Please Check Your Input")
            case 401:
                print("Unauthorized: Invalid API Key")
            case 403:
                print("Forbidden: Access Denied")
            case 404:
                print("Not Found: City Not Found")
            case 500:
                print("Internal Server Error: Please Try Again Later")
            case 502:
                print("Bad Gateway: Invalid Response From The Server")
            case 503:
                print("Service Unavailable: Server Is Down")
            case 504:
                print("Gateway Timeout: No Response From The Server")
            case _:
                print(f"HTTP Error Occurred: {http_error.title()}")

    except requests.exceptions.ConnectionError:
        print("Connection Error: Check Your Internet Connection.")

    except requests.exceptions.Timeout:
        print("Timeout Error: The Request Timed Out.")

    except requests.exceptions.TooManyRedirects:
        print("Too Many Redirects: Check The URL.")

    except requests.exceptions.RequestException as req_error:
        print(f"Request Error: {req_error.title()}")
