import pytest
import aiohttp
from aioresponses import aioresponses
from datetime import datetime
from app.openweathermap import OpenWeatherMapSDK


@pytest.fixture
def owmsdk():
    return OpenWeatherMapSDK()


@pytest.mark.asyncio
async def test_get_current_weather(owmsdk):
    city = "London"
    expected_response = {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 20.0}
    }

    with aioresponses() as m:
        m.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={owmsdk.api_key}&units=metric",
              payload=expected_response)

        response = await owmsdk.get_current_weather(city)
        assert response == expected_response


@pytest.mark.asyncio
async def test_get_forecast(owmsdk):
    city = "London"
    expected_response = {
        "list": [
            {"dt_txt": "2024-07-31 12:00:00", "main": {"temp": 22.0}},
            {"dt_txt": "2024-08-01 12:00:00", "main": {"temp": 23.0}}
        ]
    }

    with aioresponses() as m:
        m.get(f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={owmsdk.api_key}&units=metric",
              payload=expected_response)

        response = await owmsdk.get_forecast(city)
        assert response == expected_response


def test_parse_forecast(owmsdk):
    forecast_data = {
        "list": [
            {"dt_txt": "2024-07-31 12:00:00", "main": {"temp": 22.0}},
            {"dt_txt": "2024-08-01 12:00:00", "main": {"temp": 23.0}},
            {"dt_txt": "2024-08-01 15:00:00", "main": {"temp": 24.0}}
        ]
    }
    expected_output = {
        "2024-08-01": 23.5
    }

    output = owmsdk.parse_forecast(forecast_data)
    assert output == expected_output


def test_translate_description(owmsdk):
    description = "clear sky"
    expected_output = "céu limpo"

    output = owmsdk.translate_description(description)
    assert output == expected_output


def test_format_weather(owmsdk):
    city = "London"
    current_temp = 20.0
    description = "clear sky"
    forecast = {
        "2024-08-01": 23.5
    }
    expected_output = f"20°C céu limpo em London em {datetime.now().strftime('%d/%m')}. Média para os próximos dias: 24°C em 01/08."

    output = owmsdk.format_weather(city, current_temp, description, forecast)
    assert output == expected_output
