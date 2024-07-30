from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from openweathermap import OpenWeatherMapSDK

app = FastAPI()

class CityRequest(BaseModel):
    city: str

API_KEY = 'a7697db9197a006ef08d92bc02ac5d20'

@app.post("/weather")
async def get_weather(request: CityRequest):
    city = request.city
    sdk = OpenWeatherMapSDK(API_KEY)
    try:
        # Obter a temperatura atual e descrição do clima
        current_data = sdk.get_current_weather(city)
        current_temp = current_data['main']['temp']
        description = current_data['weather'][0]['description']

        # Obter a previsão do tempo
        forecast_data = sdk.get_forecast(city)
        forecast = sdk.parse_forecast(forecast_data)

        # Formatar a previsão
        formatted_weather = sdk.format_weather(city, current_temp, description, forecast)

        return {
            'formatted_weather': formatted_weather
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail="Data not found for the city")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
