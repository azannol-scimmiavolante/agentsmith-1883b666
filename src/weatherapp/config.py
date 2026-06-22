"""Configuration for WeatherApp."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
# Try multiple locations to handle different execution contexts
env_paths = [
    Path.cwd() / ".env",  # Current working directory
    Path(__file__).parent.parent.parent / ".env",  # Project root
    Path(__file__).parent / ".env",  # Package directory
]

for env_path in env_paths:
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        break
else:
    # If no .env file found, still try to load from environment
    load_dotenv()

# API Configuration
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
BASE_URL = "http://api.weatherapi.com/v1"

# Default settings
DEFAULT_CITY = "London"
