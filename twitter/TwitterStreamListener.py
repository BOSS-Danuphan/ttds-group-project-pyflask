import tweepy
from twitter.Tweet import Tweet
from storage import app_index_collection

class TwitterStreamListener(tweepy.StreamListener):
    _tweetCount = 0

    def __init__(self, api=None):
        self._tweetCount = 0
        super().__init__(api=api)

    def on_status(self, status):
        self._tweetCount += 1

        tweet = Tweet()
        tweet.Text = status.text

        app_index_collection.adddocument(tweet.Text)

        # print("***** TWEET #{0} *****".format(self._tweetCount))
        # print(tweet.Text)
        # print("\n")
        if self._tweetCount % 500 == 0:
            print('_tweetCount', self._tweetCount)

    def on_error(self, status_code):
        print("Error: {0}".format(status_code))
        if status_code == 420:
            # Enhance your calm; stop processing to avoid exponential wait time increases
            # Need better handling
            return False

    def on_limit(self, track):
        print("Limit reached")
        # Stop processing as soon as we hit a limit to avoid exponential wait time increases
        # Need better handling
        return False
