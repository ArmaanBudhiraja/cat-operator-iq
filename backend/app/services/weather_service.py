import time
import json
import logging
import urllib.request
import urllib.error
from typing import Any
from backend.app.config import settings

logger = logging.getLogger(__name__)

class WeatherService:
    """
    Fetches real-time weather data from OpenWeatherMap using WEATHER_API_KEY.
    Includes in-memory TTL caching (10 minutes) and automated fallback to realistic
    synthetic baseline data if API key is missing, network is offline, or request fails.
    """
    _cache: dict[str, Any] | None = None
    _cache_time: float = 0.0
    _CACHE_TTL_SECONDS: float = 600.0  # 10 minutes

    # Synthetic baseline for local offline operations
    FALLBACK_WEATHER: dict[str, Any] = {
        "condition": "Sunny",
        "temperature_c": 32.0,
        "wind_speed_kmh": 11.0,
        "humidity_pct": 42,
        "is_live": False,
        "source": "Synthetic Baseline"
    }

    @classmethod
    def get_weather(cls, location: str = "Peoria,US") -> dict[str, Any]:
        """
        Retrieves current weather data.
        Returns cached data if within TTL, otherwise attempts live fetch with fallback.
        """
        now = time.time()
        if cls._cache and (now - cls._cache_time) < cls._CACHE_TTL_SECONDS:
            return cls._cache

        api_key = settings.WEATHER_API_KEY
        if not api_key:
            return cls.FALLBACK_WEATHER

        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={urllib.parse.quote(location)}&appid={api_key}&units=metric"
            req = urllib.request.Request(url, headers={"User-Agent": "CAT-OperatorIQ/1.0"})
            with urllib.request.urlopen(req, timeout=4.0) as resp:
                if resp.status == 200:
                    payload = json.loads(resp.read().decode("utf-8"))
                    weather_desc = payload.get("weather", [{}])[0].get("main", "Clear")
                    temp = round(float(payload.get("main", {}).get("temp", 24.0)), 1)
                    # Convert wind speed m/s to km/h
                    wind_m_s = float(payload.get("wind", {}).get("speed", 3.0))
                    wind_kmh = round(wind_m_s * 3.6, 1)
                    humidity = int(payload.get("main", {}).get("humidity", 45))
                    city = payload.get("name", location.split(",")[0])

                    live_data = {
                        "condition": weather_desc,
                        "temperature_c": temp,
                        "wind_speed_kmh": wind_kmh,
                        "humidity_pct": humidity,
                        "is_live": True,
                        "source": f"OpenWeatherMap ({city})"
                    }
                    cls._cache = live_data
                    cls._cache_time = now
                    return live_data
        except Exception as exc:
            logger.warning(f"Weather API live fetch failed ({exc}). Rolling back to synthetic baseline.")

        # If cache exists (even expired), return it rather than abrupt change, otherwise fallback
        if cls._cache:
            return cls._cache
        return cls.FALLBACK_WEATHER
