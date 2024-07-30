from openweathermap import OpenWeatherMapSDK
import logging

logging.basicConfig(level=logging.INFO)
api_key = "a7697db9197a006ef08d92bc02ac5d20"
weather_sdk = OpenWeatherMapSDK(api_key)

city = "Sao Paulo"

try:
    current_weather = weather_sdk.get_current_weather(city)
    logging.info(f"Clima atual obtido: {current_weather}")

    forecast_data = weather_sdk.get_forecast(city)
    logging.info(f"Dados de previsão obtidos: {forecast_data}")

    forecast_avg_temps = weather_sdk.parse_forecast(forecast_data)
    logging.info(f"Previsão média diária: {forecast_avg_temps}")
except Exception as e:
    logging.error(f"Erro: {e}")
