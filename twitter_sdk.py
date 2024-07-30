import tweepy
import logging

class TwitterSDK:
    def __init__(self, api_key, api_secret_key, access_token, access_token_secret, bearer_token):
        # Autenticação com o Twitter
        self.client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret_key,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

    def send_tweet(self, message):
        try:
            # Enviar tweet usando a API v2
            response = self.client.create_tweet(text=message)
            logging.info(f"Tweet enviado com sucesso: {message}")
            return response
        except tweepy.TweepyException as e:
            logging.error(f"Erro ao enviar tweet: {e}")
            raise
