# tests/test_twitter.py
import pytest
from unittest.mock import patch, MagicMock
from app.twitter import TwitterSDK
import tweepy

@pytest.mark.asyncio
async def test_twitter_sdk_initialization():
    """
    Testa a inicialização do TwitterSDK e verifica se o cliente é configurado corretamente.
    """
    twitter_sdk = TwitterSDK()
    assert twitter_sdk.client is not None

@pytest.mark.asyncio
@patch.object(tweepy.Client, 'create_tweet', return_value={"data": {"id": "12345"}})
async def test_send_tweet(mock_create_tweet):
    """
    Testa o envio de um tweet usando mock para evitar chamadas reais à API do Twitter.
    """
    twitter_sdk = TwitterSDK()
    response = await twitter_sdk.send_tweet("Mensagem de teste")

    # Verifica se o método create_tweet foi chamado com o texto correto
    mock_create_tweet.assert_called_once_with(text="Mensagem de teste")

    # Verifica a resposta do método
    assert response["data"]["id"] == "12345"

@pytest.mark.asyncio
@patch.object(tweepy.Client, 'create_tweet', side_effect=tweepy.TweepyException("Erro ao enviar tweet"))
async def test_send_tweet_error(mock_create_tweet):
    """
    Testa o tratamento de erro ao enviar um tweet usando mock para simular uma exceção.
    """
    twitter_sdk = TwitterSDK()

    # Verifica se a exceção é levantada
    with pytest.raises(tweepy.TweepyException):
        await twitter_sdk.send_tweet("Mensagem de teste")
