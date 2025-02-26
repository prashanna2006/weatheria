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


def get_weather(gui_values):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={gui_values["search_bar"]}&appid={key}&units=imperial"
    response = requests.get(url)
    response.raise_for_status() # Raises exception for HTTP errors
    data = response.json()
    print(data)