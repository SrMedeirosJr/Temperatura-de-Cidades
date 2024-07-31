import aiohttp
import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, AsyncMock

client = TestClient(app)

@patch('app.openweathermap.OpenWeatherMapSDK.get_current_weather', new_callable=AsyncMock)
@patch('app.openweathermap.OpenWeatherMapSDK.get_forecast', new_callable=AsyncMock)
def test_get_weather(mock_get_current_weather, mock_get_forecast):
    mock_get_current_weather.return_value = {"main": {"temp": 25}, "weather": [{"description": "clear sky"}]}
    mock_get_forecast.return_value = {
        "list": [
            {"main": {"temp": 20}, "dt_txt": "2024-07-29 12:00:00"},
            {"main": {"temp": 18}, "dt_txt": "2024-07-30 12:00:00"}
        ]
    }

    response = client.post("/weather", json={"city": "TesteCity"})
    assert response.status_code == 200
    data = response.json()
    assert "formatted_weather" in data

@patch('app.openweathermap.OpenWeatherMapSDK.get_current_weather', new_callable=AsyncMock)
@patch('app.openweathermap.OpenWeatherMapSDK.get_forecast', new_callable=AsyncMock)
def test_get_weather_invalid_city(mock_get_current_weather, mock_get_forecast):
    mock_get_current_weather.side_effect = aiohttp.ClientResponseError(None, None, status=404, message="Not Found")
    mock_get_forecast.side_effect = aiohttp.ClientResponseError(None, None, status=404, message="Not Found")

    response = client.post("/weather", json={"city": "CidadeInvalida"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Erro ao obter dados do OpenWeatherMap."
