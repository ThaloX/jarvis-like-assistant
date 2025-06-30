from pathlib import Path
import requests
from src.core.logger import Logger

logger = Logger(__name__).get_logger()


class WeatherService:
    def __init__(self, default_city: str = "Cluj-Napoca"):
        logger.info("Initializing WeatherService")
        user_specific_folder = Path(__file__).parent.parent.parent / "user_data"
        api_key_path = user_specific_folder / "openweathermap_api_key"
        self.api_key = None
        if api_key_path.exists():
            with open(api_key_path, "r") as f:
                self.api_key = f.read().strip()
        else:
            logger.error(f"API key file not found at {api_key_path}")
        self.default_city = default_city

    def get_weather_info(self, city: str) -> str:
        """
        Returns weather info for a city.
        """
        if not city:
            logger.info(f"No city provided, using default city: {city}")
            city = self.default_city
        
        logger.info(f"Fetching weather for city: {city}")

        if not self.api_key:
            logger.error("Weather API key is missing! Please add it to user_data/openweathermap_api_key.")
            return "Weather API key is missing!"

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            weather = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            result = f"The weather in {city} is {weather} with a temperature of {temp}°C."
            logger.info(f"Weather result: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to fetch weather: {e}")
            return f"Sorry, I couldn't fetch the weather for {city}."
