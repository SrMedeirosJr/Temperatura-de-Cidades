import pytest
from unittest.mock import AsyncMock, patch
from app.openweathermap import OpenWeatherMapSDK

@pytest.fixture
def forecast_data():
    return {
        "list": [
            {"dt_txt": "2024-07-29 12:00:00", "main": {"temp": 25}},
            {"dt_txt": "2024-07-30 12:00:00", "main": {"temp": 30}}
        ]
    }

@patch('app.openweathermap.aiohttp.ClientSession', new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_current_weather(mock_client_session):
    # Criando um mock para a resposta
    mock_response = AsyncMock()
    mock_response.json.return_value = {
        "main": {"temp": 25},
        "weather": [{"description": "clear sky"}]
    }
    # Configurando o mock para o gerenciador de contexto assíncrono
    mock_client_session.return_value.get.return_value.__aenter__.return_value = mock_response

    sdk = OpenWeatherMapSDK()
    result = await sdk.get_current_weather("TesteCity")
    assert result["main"]["temp"] == 25
    assert result["weather"][0]["description"] == "clear sky"

@patch('app.openweathermap.aiohttp.ClientSession', new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_forecast(mock_client_session):
    # Criando um mock para a resposta
    mock_response = AsyncMock()
    mock_response.json.return_value = {"list": []}
    # Configurando o mock para o gerenciador de contexto assíncrono
    mock_client_session.return_value.get.return_value.__aenter__.return_value = mock_response

    sdk = OpenWeatherMapSDK()
    result = await sdk.get_forecast("TesteCity")
    assert result["list"] == []
