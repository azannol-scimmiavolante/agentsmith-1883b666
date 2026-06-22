"""Weather API client for WeatherApp."""

import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Optional

from weatherapp.config import WEATHER_API_KEY, BASE_URL
from weatherapp.exceptions import WeatherError
from weatherapp.models import CurrentWeather, ForecastDay, Location


class WeatherClient:
    """Client for interacting with the weather API."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the WeatherClient.

        Args:
            api_key: API key for authentication. If not provided, uses WEATHER_API_KEY from config.
        """
        self.api_key = api_key or WEATHER_API_KEY
        if not self.api_key:
            raise WeatherError("API key is required. Set WEATHER_API_KEY in .env file.")
        self.base_url = BASE_URL

    def _make_request(self, endpoint: str, params: dict) -> dict:
        """Make an HTTP request to the weather API.

        Args:
            endpoint: API endpoint (e.g., 'current.json', 'forecast.json')
            params: Query parameters for the request

        Returns:
            Parsed JSON response as a dictionary

        Raises:
            WeatherError: If the HTTP request fails or returns an error
        """
        # Add API key to parameters
        params["key"] = self.api_key

        # Build the full URL
        query_string = urllib.parse.urlencode(params)
        url = f"{self.base_url}/{endpoint}?{query_string}"

        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = response.read()
                return json.loads(data.decode("utf-8"))
        except urllib.error.HTTPError as e:
            # Read error response body if available
            error_body = e.read().decode("utf-8") if e.fp else ""
            try:
                error_data = json.loads(error_body)
                error_message = error_data.get("error", {}).get("message", str(e))
            except (json.JSONDecodeError, KeyError):
                error_message = f"HTTP {e.code}: {e.reason}"
            raise WeatherError(error_message, status_code=e.code)
        except urllib.error.URLError as e:
            raise WeatherError(f"Network error: {e.reason}")
        except json.JSONDecodeError as e:
            raise WeatherError(f"Invalid JSON response: {e}")
        except Exception as e:
            raise WeatherError(f"Unexpected error: {e}")

    def _parse_location(self, location_data: dict) -> Location:
        """Parse location data from API response.

        Args:
            location_data: Location data from API response

        Returns:
            Location object
        """
        return Location(
            name=location_data.get("name", ""),
            region=location_data.get("region", ""),
            country=location_data.get("country", ""),
            lat=location_data.get("lat", 0.0),
            lon=location_data.get("lon", 0.0),
            tz_id=location_data.get("tz_id", ""),
            localtime=location_data.get("localtime", "")
        )

    def get_current(self, city: str) -> CurrentWeather:
        """Get current weather for a city.

        Args:
            city: City name or location query

        Returns:
            CurrentWeather object with current weather data

        Raises:
            WeatherError: If the API request fails
        """
        params = {"q": city, "aqi": "no"}
        data = self._make_request("current.json", params)

        # Parse location if available
        location = None
        if "location" in data:
            location = self._parse_location(data["location"])

        # Parse current weather data
        current = data.get("current", {})
        condition_data = current.get("condition", {})

        return CurrentWeather(
            temp_c=current.get("temp_c", 0.0),
            temp_f=current.get("temp_f", 0.0),
            condition=condition_data.get("text", "Unknown"),
            humidity=current.get("humidity", 0),
            wind_kph=current.get("wind_kph", 0.0),
            uv_index=current.get("uv", 0.0),
            location=location,
            last_updated=current.get("last_updated"),
            feelslike_c=current.get("feelslike_c"),
            feelslike_f=current.get("feelslike_f"),
            wind_mph=current.get("wind_mph"),
            wind_degree=current.get("wind_degree"),
            wind_dir=current.get("wind_dir"),
            pressure_mb=current.get("pressure_mb"),
            pressure_in=current.get("pressure_in"),
            precip_mm=current.get("precip_mm"),
            precip_in=current.get("precip_in"),
            cloud=current.get("cloud"),
            vis_km=current.get("vis_km"),
            vis_miles=current.get("vis_miles"),
            gust_mph=current.get("gust_mph"),
            gust_kph=current.get("gust_kph")
        )

    def get_forecast(self, city: str, days: int = 5) -> list[ForecastDay]:
        """Get weather forecast for a city.

        Args:
            city: City name or location query
            days: Number of days to forecast (1-10, default 5)

        Returns:
            List of ForecastDay objects

        Raises:
            WeatherError: If the API request fails
        """
        # Clamp days to valid range
        days = max(1, min(days, 10))

        params = {"q": city, "days": str(days), "aqi": "no", "alerts": "no"}
        data = self._make_request("forecast.json", params)

        # Parse forecast days
        forecast_list = []
        forecast_data = data.get("forecast", {}).get("forecastday", [])

        for day_data in forecast_data:
            day_info = day_data.get("day", {})
            condition_data = day_info.get("condition", {})

            forecast_day = ForecastDay(
                date=day_data.get("date", ""),
                temp_c=day_info.get("avgtemp_c", 0.0),
                temp_f=day_info.get("avgtemp_f", 0.0),
                condition=condition_data.get("text", "Unknown"),
                humidity=day_info.get("avghumidity", 0),
                wind_kph=day_info.get("maxwind_kph", 0.0),
                uv_index=day_info.get("uv", 0.0),
                maxtemp_c=day_info.get("maxtemp_c"),
                maxtemp_f=day_info.get("maxtemp_f"),
                mintemp_c=day_info.get("mintemp_c"),
                mintemp_f=day_info.get("mintemp_f"),
                avgtemp_c=day_info.get("avgtemp_c"),
                avgtemp_f=day_info.get("avgtemp_f"),
                maxwind_mph=day_info.get("maxwind_mph"),
                maxwind_kph=day_info.get("maxwind_kph"),
                totalprecip_mm=day_info.get("totalprecip_mm"),
                totalprecip_in=day_info.get("totalprecip_in"),
                avgvis_km=day_info.get("avgvis_km"),
                avgvis_miles=day_info.get("avgvis_miles"),
                avghumidity=day_info.get("avghumidity"),
                daily_will_it_rain=day_info.get("daily_will_it_rain"),
                daily_chance_of_rain=day_info.get("daily_chance_of_rain"),
                daily_will_it_snow=day_info.get("daily_will_it_snow"),
                daily_chance_of_snow=day_info.get("daily_chance_of_snow")
            )
            forecast_list.append(forecast_day)

        return forecast_list
