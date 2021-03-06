import sys, time, json
import tweepy
from collections import namedtuple
from app.storage import app_index_collection
from app.twitter.AnalysedTweet import AnalysedTweet
from app.twitter.ImageAnalyser import ImageAnalyser

class TwitterStreamListener(tweepy.StreamListener):
    _tweetCount = 0
    _useVision = False
    _imageAnalyser = ImageAnalyser()

    def __init__(self, api=None, useVision=False):
        self._tweetCount = 0
        self._useVision = useVision
        super().__init__(api=api)

    def on_status(self, status):
        media = self.get_media(status)
        if media is None:
            return

        self._tweetCount += 1

        # Pass wanted data into analysed tweet instance
        atweet = AnalysedTweet()
        atweet.Id = status.id
        atweet.Text = status.text
        atweet.Url = media["url"]
        atweet.ImageUrl = media["media_url_https"]

        if hasattr(status, "retweeted_status"):
            atweet.OriginalId = status.retweeted_status.id

        if self._useVision:
            vision_json = self._imageAnalyser.analyse_with_ms_vision(atweet.ImageUrl)
            google_json = self._imageAnalyser.analyse_with_google_vision(atweet.ImageUrl)

            vision, google = None, None
            if vision_json is not None:
                vision = json.loads(vision_json, object_hook=lambda obj: namedtuple('result', obj.keys())(*obj.values()))
            if google_json is not None:
                google = json.loads(google_json, object_hook=lambda obj: namedtuple('result', obj.keys())(*obj.values()))

            atweet.VisionResults = vision
            atweet.GoogleResults = google


        # Add tweet to index
        app_index_collection.add_tweet(atweet)


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

    def get_media(self, status):
        if status.lang != "en":
            return

        # Exclude possibly NSFW tweets
        if hasattr(status, "possibly_sensitive") and status.possibly_sensitive:
            return

        # We only want tweets with images
        if not hasattr(status, "entities"):
            return
        entities = status.entities

        if not "media" in entities.keys():
            return
        media = entities["media"]

        if len(media) < 1:
            return

        # Photos only
        for m in media:
            if m["type"] != "photo":
                return
        if hasattr(status, "extended_entities"):
            ee = status.extended_entities
            if "media" in ee.keys():
                for m in ee["media"]:
                    if (m["type"] != "photo"):
                        return

        media = media[0]

        if not "media_url_https" in media.keys() or "url" not in media.keys():
            return

        return media