import requests
import math
import random
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List
import pandas as pd

from src.config import OPENWEATHER_API_KEY, AQICN_API_KEY, DEFAULT_CITY, DEFAULT_LAT, DEFAULT_LON, PAKISTAN_CITIES


def calculate_us_aqi_pm25(pm25: float) -> int:
    """Calculate US AQI from PM2.5 concentration (ug/m3)."""
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 500.4, 301, 500),
    ]
    for c_low, c_high, i_low, i_high in breakpoints:
        if c_low <= pm25 <= c_high:
            return round(((i_high - i_low) / (c_high - c_low)) * (pm25 - c_low) + i_low)
    if pm25 > 500.4:
        return 500
    return 0


def fetch_openweather_air_pollution(lat: float = DEFAULT_LAT, lon: float = DEFAULT_LON) -> Dict[str, Any]:
    """Fetch current air pollution data from OpenWeather API."""
    if not OPENWEATHER_API_KEY:
        return {}
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching OpenWeather Air Pollution: {e}")
    return {}


def fetch_openweather_weather(lat: float = DEFAULT_LAT, lon: float = DEFAULT_LON) -> Dict[str, Any]:
    """Fetch current weather data from OpenWeather API."""
    if not OPENWEATHER_API_KEY:
        return {}
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching OpenWeather Weather: {e}")
    return {}


def fetch_aqicn_data(city: str = DEFAULT_CITY) -> Dict[str, Any]:
    """Fetch air quality data from AQICN API."""
    if not AQICN_API_KEY:
        return {}
    url = f"https://api.waqi.info/feed/{city}/?token={AQICN_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching AQICN data: {e}")
    return {}


def generate_synthetic_observation(timestamp: datetime, city: str = DEFAULT_CITY) -> Dict[str, Any]:
    """
    Generate realistic synthetic observation for testing/fallback mode when API keys are absent.
    Uses diurnal and seasonal harmonic curves to model temperature, humidity, wind, and pollutants.
    """
    hour = timestamp.hour
    day_of_year = timestamp.timetuple().tm_yday
    
    # Temperature (celsius) diurnal & seasonal variation
    temp_base = 25.0 + 10.0 * math.sin((day_of_year - 80) * 2 * math.pi / 365)
    temp_diurnal = 5.0 * math.sin((hour - 9) * 2 * math.pi / 24)
    temperature = temp_base + temp_diurnal + random.gauss(0, 1.5)
    
    # Humidity (%) inversely proportional to temperature
    humidity = max(20.0, min(95.0, 60.0 - temp_diurnal * 4.0 + random.gauss(0, 5.0)))
    
    # Wind speed (m/s) and pressure (hPa)
    wind_speed = max(0.5, 3.5 + 2.0 * math.sin(hour * 2 * math.pi / 24) + random.gauss(0, 0.8))
    pressure = 1013.25 + random.gauss(0, 3.0)
    
    # Pollutants (ug/m3) - peak during rush hours (8am and 8pm)
    rush_hour_effect = math.exp(-((hour - 8)**2)/8.0) + math.exp(-((hour - 20)**2)/8.0)
    pm25 = max(5.0, 35.0 + 40.0 * rush_hour_effect + (100.0 - humidity)*0.3 + random.gauss(0, 8.0))
    pm10 = pm25 * (1.5 + random.uniform(0.1, 0.4))
    no2 = max(2.0, 20.0 + 25.0 * rush_hour_effect + random.gauss(0, 4.0))
    so2 = max(1.0, 8.0 + 5.0 * random.random())
    co = max(0.2, 0.8 + 1.2 * rush_hour_effect + random.gauss(0, 0.1))
    o3 = max(5.0, 30.0 + 25.0 * math.sin((hour - 12) * 2 * math.pi / 24) + random.gauss(0, 5.0))
    
    aqi = calculate_us_aqi_pm25(pm25)
    
    return {
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "city": city,
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "wind_speed": round(wind_speed, 2),
        "pressure": round(pressure, 2),
        "pm25": round(pm25, 2),
        "pm10": round(pm10, 2),
        "no2": round(no2, 2),
        "so2": round(so2, 2),
        "co": round(co, 2),
        "o3": round(o3, 2),
        "aqi": aqi
    }


def get_current_raw_data(city: str = DEFAULT_CITY, lat: float = None, lon: float = None) -> Dict[str, Any]:
    """Fetch current raw observation from API or synthetic fallback for any Pakistan city."""
    if city in PAKISTAN_CITIES:
        lat = lat or PAKISTAN_CITIES[city]["lat"]
        lon = lon or PAKISTAN_CITIES[city]["lon"]
    else:
        lat = lat or DEFAULT_LAT
        lon = lon or DEFAULT_LON

    now = datetime.now(timezone.utc)
    ow_pollution = fetch_openweather_air_pollution(lat, lon)
    ow_weather = fetch_openweather_weather(lat, lon)
    
    if ow_pollution and ow_weather and "list" in ow_pollution and len(ow_pollution["list"]) > 0:
        comp = ow_pollution["list"][0]["components"]
        main_weather = ow_weather.get("main", {})
        wind = ow_weather.get("wind", {})
        
        pm25 = comp.get("pm2_5", 25.0)
        return {
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "city": city,
            "temperature": round(main_weather.get("temp", 25.0), 2),
            "humidity": round(main_weather.get("humidity", 50.0), 2),
            "wind_speed": round(wind.get("speed", 3.0), 2),
            "pressure": round(main_weather.get("pressure", 1013.0), 2),
            "pm25": round(pm25, 2),
            "pm10": round(comp.get("pm10", 40.0), 2),
            "no2": round(comp.get("no2", 20.0), 2),
            "so2": round(comp.get("so2", 5.0), 2),
            "co": round(comp.get("co", 500.0) / 1000.0, 2),  # convert ug/m3 to mg/m3 approx
            "o3": round(comp.get("o3", 30.0), 2),
            "aqi": calculate_us_aqi_pm25(pm25)
        }
        
    # AQICN fallback
    aqicn = fetch_aqicn_data(city)
    if aqicn and aqicn.get("status") == "ok":
        iaqi = aqicn.get("data", {}).get("iaqi", {})
        pm25_val = iaqi.get("pm25", {}).get("v", 35.0)
        return {
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "city": city,
            "temperature": round(iaqi.get("t", {}).get("v", 25.0), 2),
            "humidity": round(iaqi.get("h", {}).get("v", 50.0), 2),
            "wind_speed": round(iaqi.get("w", {}).get("v", 3.0), 2),
            "pressure": round(iaqi.get("p", {}).get("v", 1013.0), 2),
            "pm25": round(pm25_val, 2),
            "pm10": round(iaqi.get("pm10", {}).get("v", 50.0), 2),
            "no2": round(iaqi.get("no2", {}).get("v", 20.0), 2),
            "so2": round(iaqi.get("so2", {}).get("v", 5.0), 2),
            "co": round(iaqi.get("co", {}).get("v", 1.0), 2),
            "o3": round(iaqi.get("o3", {}).get("v", 30.0), 2),
            "aqi": int(aqicn.get("data", {}).get("aqi", calculate_us_aqi_pm25(pm25_val)))
        }

    # Synthetic observation fallback
    return generate_synthetic_observation(now, city)
