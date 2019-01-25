import tweepy
from app import app
from app.twitter.TwitterStreamListener import TwitterStreamListener

class TwitterStreamBuilder():
    @staticmethod
    def BuildApiClient():
        auth = tweepy.OAuthHandler(app.config['TWITTER_CONSUMER_KEY'], app.config['TWITTER_CONSUMER_SECRET'])
        auth.set_access_token(app.config['TWITTER_ACCESS_TOKEN_KEY'], app.config['TWITTER_ACCESS_TOKEN_SECRET'])
        return tweepy.API(auth)

    @staticmethod
    def StreamBuilder():
        api = TwitterStreamBuilder.BuildApiClient()
        streamListener = TwitterStreamListener(api)
        myStream = tweepy.Stream(auth = api.auth, listener=streamListener)
        return myStream