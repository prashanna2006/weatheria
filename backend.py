import flet as ft
import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

load_dotenv()
key = os.getenv('API_KEY')

def get_weather(gui_values):
    print(gui_values)