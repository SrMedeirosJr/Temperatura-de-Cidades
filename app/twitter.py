import tweepy
import logging
from config import (
    TWITTER_API_KEY,
    TWITTER_API_SECRET_KEY,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_BEARER_TOKEN
)


class TwitterSDK:
    def __init__(self):
        try:
            self.client = tweepy.Client(
                bearer_token=TWITTER_BEARER_TOKEN,
                consumer_key=TWITTER_API_KEY,
                consumer_secret=TWITTER_API_SECRET_KEY,
                access_token=TWITTER_ACCESS_TOKEN,
                access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
            )
            logging.info("Autenticação com o Twitter realizada com sucesso.")
        except tweepy.TweepyException as e:
            logging.error(f"Erro ao autenticar com o Twitter: {e}")
        except Exception as e:
            logging.critical(f"Erro inesperado ao autenticar com o Twitter: {str(e)}")


    async def send_tweet(self, message: str) -> dict:

        try:
            response = self.client.create_tweet(text=message)
            logging.info(f"Tweet enviado com sucesso: {message}")
            return response
        except tweepy.TweepyException as e:
            logging.error(f"Erro ao enviar tweet: {e}")
        except Exception as e:
            logging.critical(f"Erro inesperado ao enviar tweet: {str(e)}")

