from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from .openweathermap import OpenWeatherMapSDK
from .twitter import TwitterSDK
import aiohttp
import logging


logging.basicConfig(level=logging.INFO)


app = FastAPI(
    title="Tweet por Temperatura API",
    description="API para obter informações meteorológicas e postar atualizações no Twitter.",
    version="1.0.0",
    docs_url="/docs"
)


class CityRequest(BaseModel):
    city: str


@app.post("/weather", summary="Obter clima e enviar tweet",
          description="Informe o nome da cidade para obter o clima atual e a previsão dos próximos dias, e enviar um tweet.")
async def get_weather(request: CityRequest):

    sdk = OpenWeatherMapSDK()
    twitter_sdk = TwitterSDK()

    try:

        current_data = await sdk.get_current_weather(request.city)
        current_temp = current_data['main']['temp']
        description = current_data['weather'][0]['description']


        forecast_data = await sdk.get_forecast(request.city)
        forecast = sdk.parse_forecast(forecast_data)


        formatted_weather = sdk.format_weather(request.city, current_temp, description, forecast)


        await twitter_sdk.send_tweet(formatted_weather)

        return {'formatted_weather': formatted_weather}
    except aiohttp.ClientResponseError as e:
        logging.error(f"Erro na resposta do cliente: {e.status} {e.message}")
        raise HTTPException(status_code=e.status, detail="Erro ao obter dados do OpenWeatherMap.")
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
