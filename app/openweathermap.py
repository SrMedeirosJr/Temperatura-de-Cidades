import aiohttp
import logging
from datetime import datetime
from config import OPENWEATHER_API_KEY

class OpenWeatherMapSDK:
    def __init__(self):

        self.api_key = OPENWEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5/"

    async def get_current_weather(self, city: str) -> dict:

        url = f"{self.base_url}weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            logging.error(f"Erro ao se comunicar com a API OpenWeatherMap: {e}")
            raise

    async def get_forecast(self, city: str) -> dict:

        url = f"{self.base_url}forecast"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            logging.error(f"Erro ao se comunicar com a API OpenWeatherMap: {e}")
            raise

    def parse_forecast(self, forecast_data: dict) -> dict:

        daily_temps = {}
        today = datetime.now().strftime('%Y-%m-%d')
        for entry in forecast_data['list']:
            date = entry['dt_txt'].split(' ')[0]
            if date == today:
                continue  # Ignorar a data de hoje
            temp = entry['main']['temp']
            if date not in daily_temps:
                daily_temps[date] = []
            daily_temps[date].append(temp)

        daily_avg_temps = {date: sum(temps) / len(temps) for date, temps in daily_temps.items()}
        return daily_avg_temps

    def translate_description(self, description: str) -> str:

        translations = {
            "light intensity drizzle": "chuvisco leve",
            "clear sky": "céu limpo",
            "few clouds": "poucas nuvens",
            "scattered clouds": "nuvens dispersas",
            "broken clouds": "nuvens quebradas",
            "shower rain": "chuva de banho",
            "rain": "chuva",
            "thunderstorm": "trovoada",
            "snow": "neve",
            "mist": "névoa"
        }
        return translations.get(description, description)

    def format_weather(self, city: str, current_temp: float, description: str, forecast: dict) -> str:
        today = datetime.now().strftime('%d/%m')
        description_pt = self.translate_description(description)
        forecast_str = ", ".join([f"{temp:.0f}°C em {datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m')}" for date, temp in forecast.items()])

        return f"{current_temp:.0f}°C {description_pt} em {city} em {today}. Média para os próximos dias: {forecast_str}."
