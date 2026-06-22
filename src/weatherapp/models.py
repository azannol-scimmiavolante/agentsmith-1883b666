"""Data models for WeatherApp."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Location:
    """Represents a geographic location."""
    name: str
    region: str
    country: str
    lat: float
    lon: float
    tz_id: str
    localtime: str


@dataclass
class CurrentWeather:
    """Represents current weather conditions."""
    temp_c: float
    temp_f: float
    condition: str
    humidity: int
    wind_kph: float
    uv_index: float
    location: Optional[Location] = None
    last_updated: Optional[str] = None
    feelslike_c: Optional[float] = None
    feelslike_f: Optional[float] = None
    wind_mph: Optional[float] = None
    wind_degree: Optional[int] = None
    wind_dir: Optional[str] = None
    pressure_mb: Optional[float] = None
    pressure_in: Optional[float] = None
    precip_mm: Optional[float] = None
    precip_in: Optional[float] = None
    cloud: Optional[int] = None
    vis_km: Optional[float] = None
    vis_miles: Optional[float] = None
    gust_mph: Optional[float] = None
    gust_kph: Optional[float] = None


@dataclass
class ForecastDay:
    """Represents a single day's weather forecast."""
    date: str
    temp_c: float
    temp_f: float
    condition: str
    humidity: int
    wind_kph: float
    uv_index: float
    maxtemp_c: Optional[float] = None
    maxtemp_f: Optional[float] = None
    mintemp_c: Optional[float] = None
    mintemp_f: Optional[float] = None
    avgtemp_c: Optional[float] = None
    avgtemp_f: Optional[float] = None
    maxwind_mph: Optional[float] = None
    maxwind_kph: Optional[float] = None
    totalprecip_mm: Optional[float] = None
    totalprecip_in: Optional[float] = None
    avgvis_km: Optional[float] = None
    avgvis_miles: Optional[float] = None
    avghumidity: Optional[int] = None
    daily_will_it_rain: Optional[int] = None
    daily_chance_of_rain: Optional[int] = None
    daily_will_it_snow: Optional[int] = None
    daily_chance_of_snow: Optional[int] = None
