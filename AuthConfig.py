import configparser

import tweepy
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class AuthConfig:

    __config = configparser.RawConfigParser()
    __config.read("app_bot.properties")

    __consumer_key = __config.get("Consumer", "CONSUMER_KEY")
    __consumer_secret = __config.get("Consumer", "CONSUMER_SECRET")
    __bearer_token = __config.get("Bearer", "BEARER_TOKEN")
    __access_token = __config.get("AccessToken", "ACCESS_TOKEN")
    __access_token_secret = __config.get("AccessToken", "ACCESS_TOKEN_SECRET")

    __api = None

    def __init__(self):
        self.auth = tweepy.OAuth1UserHandler(
            consumer_key=self.__consumer_key,
            consumer_secret=self.__consumer_secret,
            access_token=self.__access_token,
            access_token_secret=self.__access_token_secret
        )

        self.__api = tweepy.API(self.auth)

    def get_api(self):
        try:
            user = self.__api.verify_credentials()
            if user:
                return self.__api
            raise ValueError("Invalid credentials provided.")

        except Exception as e:
            logger.log("Error when verifying credentials.", str(e))

    def get_mentions(self, since_id):
        return tweepy.Cursor(self.__api.mentions_timeline, since_id=since_id).items()

    def get_timeline(self):
        return tweepy.Cursor(self.__api.user_timeline).items()