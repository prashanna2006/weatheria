import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

load_dotenv()
key = os.getenv('API_KEY')


def default_values(gui_values):

    defaults = {
    "temp_unit": "\u00B0F",
    "search_bar": None,
    "city_name": "City_Name",
    "current_temp": "--\u00B0F",
    "max_temp": "--\u00B0F",
    "min_temp": "--\u00B0F",
    "weather_desc": "Weather Description",
    "feels_like": f"Feels like --°F",
    "sunrise": "--:-- AM",
    "sunset": "--:-- PM",
    "wind_speed": f"-- km/hr",
    "humidity": f"-- %",
    "pressure": f"-- hPa",
    "visibility": f"---- m",
    "sea_lvl": f"---- m",
    "ground_lvl": f"---- m",
    }

    for key in gui_values.keys():
        if (key == "error"):
            pass
        elif (key == "temp_unit"):
            gui_values[key].text = defaults[key]
            gui_values[key].update()
        else:
            gui_values[key].value = defaults[key]
            gui_values[key].update()


def error_display(error, gui_values):
    gui_values["error"].value = error
    gui_values["error"].update()
    default_values(gui_values)


def timezone_convert(timestamp, timezone_offset):
    utc_time = datetime.fromtimestamp(timestamp, tz = timezone.utc)
    local_time = utc_time + timedelta(seconds = timezone_offset)
    return local_time.strftime('%I:%M %p')


def temp_conversion(temps):
    celscius_temps = []

    for temp in temps:
        celscius_temps.append((5*(temp-32)/9))
    return celscius_temps


def display_weather(data, gui_values, timezone):

    current_temp = (data["main"]["temp"])
    max_temp = (data["main"]["temp_max"])
    min_temp = (data["main"]["temp_min"])
    feels_like = data["main"]["feels_like"]
    temps = [current_temp, max_temp, min_temp, feels_like]

    if gui_values["temp_unit"].text == "\u00B0C":
        current_temp, max_temp, min_temp, feels_like = temp_conversion(temps)

    api_values = {
        "city_name": f'{data["name"]}, {data["sys"]["country"]}',
        "current_temp": f"{round(current_temp)}{gui_values["temp_unit"].text}",
        "max_temp": f"{round(max_temp)}{gui_values["temp_unit"].text}",
        "min_temp": f"{round(min_temp)}{gui_values["temp_unit"].text}",
        "weather_desc": f'{data["weather"][0]["description"]}'.title(),
        "feels_like": f'Feels like: {round(feels_like)}{gui_values["temp_unit"].text}',
        "sunrise": timezone_convert(data["sys"]["sunrise"], timezone),
        "sunset": timezone_convert(data["sys"]["sunset"], timezone),
        "wind_speed": f'{data["wind"]["speed"]} km/hr',
        "humidity": f'{data["main"]["humidity"]} %',
        "pressure": f'{data["main"]["pressure"]} hPa',
        "visibility": f'{data["visibility"]} m',
        "sea_lvl": f'{data["main"]["sea_level"]} m',
        "ground_lvl": f'{data["main"]["grnd_level"]} m',
    }

    for key in api_values.keys():
        gui_values[key].value = api_values[key]
        gui_values[key].update()
    gui_values["search_bar"].value = None
    gui_values["search_bar"].update()
    gui_values["error"].value = None
    gui_values["error"].update()


def get_weather(gui_values):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={gui_values["search_bar"].value}&appid={key}&units=imperial"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data["cod"] == 200:
            display_weather(data, gui_values, data["timezone"])
            
    except requests.exceptions.HTTPError as http_error:
        status_code = response.status_code
        match status_code:
            case 400:
                error = "Bad Request: Please Check Your Input"
            case 401:
                error = "Unauthorized: Invalid API Key"
            case 403:
                error = "Forbidden: Access Denied"
            case 404:
                error = "Not Found: City Not Found"
            case 500:
                error = "Internal Server Error: Please Try Again Later"
            case 502:
                error = "Bad Gateway: Invalid Response From The Server"
            case 503:
                error = "Service Unavailable: Server Is Down"
            case 504:
                error = "Gateway Timeout: No Response From The Server"
            case _:
                error = f"HTTP Error Occurred: {http_error.title()}"
        error_display(error, gui_values)

    except requests.exceptions.ConnectionError:
        error = "Connection Error: Check Your Internet Connection."
        error_display(error, gui_values)

    except requests.exceptions.Timeout:
        error = "Timeout Error: The Request Timed Out."
        error_display(error, gui_values)

    except requests.exceptions.TooManyRedirects:
        error = "Too Many Redirects: Check The URL."
        error_display(error, gui_values)

    except requests.exceptions.RequestException as req_error:
        error = f"Request Error: {req_error.title()}"
        error_display(error, gui_values)
