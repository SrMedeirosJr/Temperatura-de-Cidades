import requests
import logging
from datetime import datetime

class OpenWeatherMapSDK:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/"

    def get_current_weather(self, city):
        url = f"{self.base_url}weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao obter clima atual: {e}")
            raise

    def get_forecast(self, city):
        url = f"{self.base_url}forecast"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao obter previsão do tempo: {e}")
            raise

    def parse_forecast(self, forecast_data):
        daily_temps = {}
        today = datetime.now().strftime('%Y-%m-%d')
        for entry in forecast_data['list']:
            date = entry['dt_txt'].split(' ')[0]
            if date == today:
                continue  # Skip today's date
            temp = entry['main']['temp']
            if date not in daily_temps:
                daily_temps[date] = []
            daily_temps[date].append(temp)

        daily_avg_temps = {date: sum(temps) / len(temps) for date, temps in daily_temps.items()}
        return daily_avg_temps

    def translate_description(self, description):
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

    def format_weather(self, city, current_temp, description, forecast):
        today = datetime.now().strftime('%d/%m')
        description_pt = self.translate_description(description)
        forecast_str = ""
        for date, temp in forecast.items():
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date_str = date_obj.strftime('%d/%m')
            forecast_str += f"{temp:.0f}°C em {date_str}, "

        forecast_str = forecast_str.rstrip(', ')
        result = f"{current_temp:.0f}°C e {description_pt} em {city} em {today}. Média para os próximos dias: {forecast_str}."
        return result
