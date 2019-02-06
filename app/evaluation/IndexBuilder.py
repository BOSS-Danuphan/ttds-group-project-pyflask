from app.models.IndexCollection import IndexCollection
from app.api.Search import SearchEngine
from app.twitter.AnalysedTweet import AnalysedTweet
from app.evaluation.EvalResult import EvalResult
import math

class IndexBuilder():
    
    def __init__(self, use_google=False, use_ms=False, google_confidence = 0.5, ms_confidence=0.5, use_stemming=True, use_stopping=True):
        self.index = IndexCollection(use_google=use_google, use_ms=use_ms, google_confidence = google_confidence, ms_confidence=ms_confidence, use_stemming=use_stemming, use_stopping=use_stopping)

    def load(self, examples):
        for example in examples:
            tweet = self.buildTweetModel(example)
            if tweet is not None:
                self.index.add_tweet(tweet)

        return self.index

    def buildTweetModel(self, example):        
        media = self.get_media(example)
        
        if media is None:
            return None

        tweet = AnalysedTweet()
        tweet.Id = example.id
        tweet.Text = example.text
        tweet.Url = media.url

        if hasattr(example, "retweeted_status"):
            tweet.OriginalId = example.retweeted_status.id

        tweet.ImageUrl = media.media_url_https
        tweet.VisionResults = example.vision_results
        tweet.GoogleResults = example.google_results
        return tweet
    
    def get_media(self, tweet_json):
        if tweet_json.lang != "en":
            return

        # Exclude possibly NSFW tweets
        if hasattr(tweet_json, "possibly_sensitive") and tweet_json.possibly_sensitive:
            return
        
        # We only want tweets with images
        if not hasattr(tweet_json, "entities"):
            return
        entities = tweet_json.entities
        
        if not hasattr(entities, "media"):
            return
        
        media = entities.media

        if len(media) < 1:
            return

        # Photos only
        for m in media:
            if m.type != "photo":
                return

        # Allow non-photos
        # if hasattr(tweet_json, "extended_entities"):
        #     ee = tweet_json.extended_entities
        #     if hasattr(ee, "media"):
        #         for m in ee.media:
        #             if (m.type != "photo"):
        #                 print('non-photo')
        #                 return

        media = media[0]

        return media
