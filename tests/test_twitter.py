import pytest
from unittest.mock import patch, MagicMock
from app.twitter import TwitterSDK
import tweepy


def test_twitter_sdk_initialization():
    """
    Testa a inicialização do TwitterSDK e verifica se o cliente é configurado corretamente.
    """
    try:
        twitter_sdk = TwitterSDK()
        assert twitter_sdk.client is not None
    except Exception as e:
        pytest.fail(f"Falha ao inicializar TwitterSDK: {e}")


@patch('app.twitter_sdk.TwitterSDK.client', new_callable=MagicMock)
def test_send_tweet(mock_client):
    """
    Testa o envio de um tweet usando mock para evitar chamadas reais à API do Twitter.
    """
    # Configura o mock para retornar uma resposta simulada
    mock_client.create_tweet.return_value = {"data": {"id": "12345"}}

    twitter_sdk = TwitterSDK()
    response = twitter_sdk.send_tweet("Mensagem de teste")

    # Verifica se o método create_tweet foi chamado com o texto correto
    mock_client.create_tweet.assert_called_once_with(text="Mensagem de teste")

    # Verifica a resposta do método
    assert response["data"]["id"] == "12345"


@patch('app.twitter_sdk.TwitterSDK.client', new_callable=MagicMock)
def test_send_tweet_error(mock_client):
    """
    Testa o tratamento de erro ao enviar um tweet usando mock para simular uma exceção.
    """
    # Configura o mock para lançar uma exceção quando create_tweet é chamado
    mock_client.create_tweet.side_effect = tweepy.TweepyException("Erro ao enviar tweet")

    twitter_sdk = TwitterSDK()

    # Verifica se a exceção é levantada
    with pytest.raises(tweepy.TweepyException):
        twitter_sdk.send_tweet("Mensagem de teste")
