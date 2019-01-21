import tweepy
from app import app
from app.twitter.TwitterStreamListener import TwitterStreamListener

class TwitterStreamBuilder():
    # From http://techland.time.com/2009/06/08/the-500-most-frequently-used-words-on-twitter/
    topTerms = ['the','i','to','a','and','is','in','it','you','of','tinyurl.com','for','on','my','\'s','that','at','with','me','do']

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
