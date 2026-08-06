import os
from dotenv import load_dotenv

load_dotenv()

# Hopsworks Configuration
HOPSWORKS_API_KEY = os.getenv("HOPSWORKS_API_KEY", "")
HOPSWORKS_PROJECT_NAME = os.getenv("HOPSWORKS_PROJECT_NAME", "aqi_predictor_10pearls")

# Weather / AQI API Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
AQICN_API_KEY = os.getenv("AQICN_API_KEY", "")

# Default Target Location (Whole Pakistan Support)
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Lahore")
DEFAULT_LAT = float(os.getenv("DEFAULT_LAT", "31.5204"))
DEFAULT_LON = float(os.getenv("DEFAULT_LON", "74.3587"))

PAKISTAN_CITIES = {
    "Lahore": {"lat": 31.5204, "lon": 74.3587, "province": "Punjab"},
    "Karachi": {"lat": 24.8607, "lon": 67.0011, "province": "Sindh"},
    "Islamabad": {"lat": 33.6844, "lon": 73.0479, "province": "Capital"},
    "Rawalpindi": {"lat": 33.5651, "lon": 73.0169, "province": "Punjab"},
    "Peshawar": {"lat": 34.0151, "lon": 71.5249, "province": "KPK"},
    "Quetta": {"lat": 30.1798, "lon": 66.9750, "province": "Balochistan"},
    "Multan": {"lat": 30.1575, "lon": 71.5249, "province": "Punjab"},
    "Faisalabad": {"lat": 31.4504, "lon": 73.1350, "province": "Punjab"},
    "Sialkot": {"lat": 32.4945, "lon": 74.5229, "province": "Punjab"},
    "Gujranwala": {"lat": 32.1877, "lon": 74.1945, "province": "Punjab"},
    "Hyderabad": {"lat": 25.3960, "lon": 68.3578, "province": "Sindh"}
}

# Feature Group Configuration
FEATURE_GROUP_NAME = "aqi_weather_features"
FEATURE_GROUP_VERSION = 1
MODEL_NAME = "aqi_3day_forecast_model"
MODEL_VERSION = 1

# Hazardous AQI Alert Thresholds (US AQI Standard)
AQI_THRESHOLDS = {
    "GOOD": (0, 50),
    "MODERATE": (51, 100),
    "UNHEALTHY_SENSITIVE": (101, 150),
    "UNHEALTHY": (151, 200),
    "VERY_UNHEALTHY": (201, 300),
    "HAZARDOUS": (301, 500)
}
