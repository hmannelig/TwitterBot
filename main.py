import threading
import uuid
import time
import logging

from AuthConfig import AuthConfig

logger = logging.getLogger()
logger.setLevel(level=logging.INFO)

file_path = "since_id.txt"


def store_new_since_id(since_id):

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(since_id))
        f.close()


def get_since_id() -> int:
    from os.path import exists

    file_exists = exists(file_path)
    since_id = 1

    if file_exists:
        with open(file_path, encoding='utf-8') as f:
            since_id = int(f.read())
            f.close()
    else:
        store_new_since_id(since_id)

    return since_id


class TwitterBot:
    __twitter_api = None
    __auth_config = AuthConfig()

    def __init__(self):

        self.__twitter_api = self.__auth_config.get_api()

    def __publish_tweet(self, tweet_text=""):
        self.__twitter_api.update_status(tweet_text)

    def __reply_to(self, tweet_text="", tweet_id=None):
        if tweet_id:
            self.__twitter_api.update_status(tweet_text,
                                             in_reply_to_status_id=tweet_id,
                                             auto_populate_reply_metadata=True)

    def tweet(self):

        while True:
            string = str(uuid.uuid4())
            logger.info(str.format("Publishing new tweet: {}", string))
            self.__publish_tweet(string)
            logger.info("Tweet published, see you in 30 minutes...")
            time.sleep(1800)

    def run_bot(self):
        threading.Thread(target=self.listen_for_mentions).start()
        threading.Thread(target=self.tweet).start()

    def listen_for_mentions(self):

        since_id = get_since_id()

        while True:
            logger.info("Checking for mentions...")
            since_id = self.check_mentions(since_id)
            store_new_since_id(since_id)
            logger.info("Mentions checked, sleeping 1 minute...")
            time.sleep(60)

    def check_mentions(self, since_id) -> int:
        logger.info("Getting mentions...")
        new_since_id = since_id
        mentions = self.__auth_config.get_mentions(since_id=since_id)
        for tweet in mentions:
            print(tweet)

            new_since_id = max(tweet.id, new_since_id)
            logger.info(f'Next since ID {new_since_id} ')

            # if tweet.in_reply_to_status_id is None:
                #continue
            logger.info(f"Answering to {tweet.user.name}")
            self.__reply_to(tweet_text="Hola gracias por mencionarme uwu" + str(uuid.uuid4()),
                            tweet_id=tweet.id)

            if not tweet.favorited:
                tweet.favorite()

        return new_since_id

    def delete_timeline(self):
        print("Deleting tweets for account @%s" % self.__auth_config.get_api().verify_credentials().screen_name)
        timeline = self.__auth_config.get_timeline()

        for status in timeline:
            try:
                self.__auth_config.get_api().destroy_status(status.id)
                logger.info("Deleted", status.id)
            except Exception as e:
                logger.info("Failed to delete tweet", status.id)


def main():
    twitter_bot = TwitterBot()
    twitter_bot.run_bot()


main()
