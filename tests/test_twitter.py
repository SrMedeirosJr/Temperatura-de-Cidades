import pytest
from unittest.mock import patch, MagicMock
from app.twitter import TwitterSDK
import tweepy

@pytest.mark.asyncio
async def test_twitter_sdk_initialization():

    twitter_sdk = TwitterSDK()
    assert twitter_sdk.client is not None

@pytest.mark.asyncio
@patch.object(tweepy.Client, 'create_tweet', return_value={"data": {"id": "12345"}})
async def test_send_tweet(mock_create_tweet):

    twitter_sdk = TwitterSDK()
    response = await twitter_sdk.send_tweet("Mensagem de teste")


    mock_create_tweet.assert_called_once_with(text="Mensagem de teste")


    assert response["data"]["id"] == "12345"

@pytest.mark.asyncio
@patch.object(tweepy.Client, 'create_tweet', side_effect=tweepy.TweepyException("Erro ao enviar tweet"))
async def test_send_tweet_error(mock_create_tweet):

    twitter_sdk = TwitterSDK()


    with pytest.raises(tweepy.TweepyException):
        await twitter_sdk.send_tweet("Mensagem de teste")
