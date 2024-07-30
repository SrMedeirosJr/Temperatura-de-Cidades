from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from openweathermap import OpenWeatherMapSDK
from twitter_sdk import TwitterSDK  # Importar o SDK do Twitter
import tweepy  # Importar o tweepy

app = FastAPI()

class CityRequest(BaseModel):
    city: str

API_KEY = 'a7697db9197a006ef08d92bc02ac5d20'
TWITTER_API_KEY = 'jonKg4RgO8rVY3JJrI6QD8XVw'
TWITTER_API_SECRET_KEY = 'UIK8w0vaNqf1JEL6EJOyHVNspzX9Jxqs5YrBKliarMJfxs2Stl'
TWITTER_ACCESS_TOKEN = '1818062877577666560-23jEdwOR9U2Oi6ACOv3h8jVrrb3AB4'
TWITTER_ACCESS_TOKEN_SECRET = 'fHSZaiaqmXlRWxQ9eQQAgIbqxig7efp15QCDGsLiX18Zq'
TWITTER_BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAMlnvAEAAAAA3CQqqdpIQJ1xKY060bzY9B9KjtY%3DPQGvZsDdpWoCl8Y8O7WBFrJOMC2xsDAjD8XRi4XXL7kYLllWbj'

@app.post("/weather")
async def get_weather(request: CityRequest):
    city = request.city
    sdk = OpenWeatherMapSDK(API_KEY)
    twitter_sdk = TwitterSDK(TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_BEARER_TOKEN)

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

        # Enviar tweet com a previsão do tempo
        twitter_sdk.send_tweet(formatted_weather)

        return {
            'formatted_weather': formatted_weather
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail="Data not found for the city")
    except tweepy.TweepyException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar tweet: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
