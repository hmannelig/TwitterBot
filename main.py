import tweepy
import configparser

config = configparser.RawConfigParser()
config.read("app_bot.properties")

consumer_key = config.get("Consumer", "CONSUMER_KEY")
consumer_secret = config.get("Consumer", "CONSUMER_SECRET")

bearer_token = config.get("Bearer", "BEARER_TOKEN")

access_token = config.get("AccessToken", "ACCESS_TOKEN")
access_token_secret = config.get("AccessToken", "ACCESS_TOKEN_SECRET")
#
# client = tweepy.Client(
#     bearer_token=bearer_token,
#     consumer_key=consumer_key,
#     consumer_secret=consumer_secret,
#     access_token=access_token,
#     access_token_secret=access_token_secret)

client = tweepy.Client(bearer_token=bearer_token)

try:
    # query = 'from:yawylno -is:retweet'
    # query = 'from:TristVillalba -is:retweet'
    query = 'from:Alm0hada -is:retweet'

    tweets = client.search_recent_tweets(query=query,
                                         tweet_fields=['context_annotations', 'created_at'],
                                         max_results=100)
    #
    # tweets = client.(query=query,
    #                                   tweet_fields=['context_annotations', 'created_at'],
    #                                   max_results=100)

    # tweets = tweepy.Paginator(client.search_all_tweets(
    #     query=query,
    #     tweet_fields=['context_annotations', 'created_at'],
    #     max_results=100)
    # ).flatten(limit=1000)

    for tweet in tweets.data:
        # client.delete_tweet(id=tweet.id)
        print(tweet.text)
    # client.create_tweet(text="aaa")

except Exception as e:
    print("Couldn't verify credentials", str(e))

# auth = tweepy.OAuth1UserHandler(
#     consumer_key=consumer_key,
#     consumer_secret=consumer_secret,
#     access_token=access_token,
#     access_token_secret=access_token_secret
# )
#
# api = tweepy.API(auth)
#
# try:
#     user = api.verify_credentials()
#
#     if user:
#         # api.update_status("@Alm0hada")
#         api.update_status("@Alm0hada this bot uses python")
# except Exception as e:
#     print("Couldn't verify credentials", str(e))

# print("Deleting tweets for account @%s" % api.verify_credentials().screen_name)
#
# for status in tweepy.Cursor(api.user_timeline).items():
#     try:
#         api.destroy_status(status.id)
#         print ("Deleted", status.id)
#     except Exception as e:
#         print("Failed to delete tweet", status.id)
