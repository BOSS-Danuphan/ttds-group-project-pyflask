from app.api.processor import PreProcessor
from app.twitter.AnalysedTweet import AnalysedTweet
from collections import defaultdict
import json

class IndexCollection():
    '''This class aims to keep search index in memory'''
    _loaded=None
    _tweet_count=0
    _initial_tweet_count=0
    _export_frequency = 100

    def __init__(self, fileService=None, use_google=False, use_ms=False, google_confidence = 0.5, ms_confidence=0.5, use_stemming=True, use_stopping=True):
        self.index = defaultdict(list)
        self.preprocesser = PreProcessor(apply_stemming=use_stemming, apply_stopping=use_stopping)
        self.fileService = fileService
        
        self.use_google = use_google
        self.google_confidence = google_confidence

        self.use_ms = use_ms
        self.ms_confidence = ms_confidence

        self.validate_confidence("google_confience", google_confidence)
        self.validate_confidence("ms_confidence", ms_confidence)
        
        if self.fileService is not None:
            self.load()

    def load(self):
        if self.fileService is None:
            return

        serialized_index = self.fileService.read()
        if serialized_index and len(serialized_index) > 2:
            json_dict = json.loads(serialized_index)
            self._tweet_count = self._initial_tweet_count = int(json_dict["tweet_count"])
            self.index = defaultdict(list, json_dict["index"])

        self._loaded = True

    def add_tweet(self, tweet):
        self._tweet_count += 1
        if (self._tweet_count % self._export_frequency == 0):
            self.export()

        tweetID = tweet.OriginalId  if tweet.OriginalId is not None else tweet.Id
        
        # Index tweet text
        terms = self.preprocesser.preprocess(tweet.Text)
        if terms is None:
            # Preprocessor returns None if tweet contains offensive terms. Stop processing.
            return

        for key in terms:
            if tweetID not in self.index[key]:
                self.index[key].insert(0,tweetID)

        if self.use_ms and tweet.VisionResults is not None:
            """tags: cut above the confidence 50
                key of list of dictionaries with 'confidence' and 'name'"""
            # Indexing MS Results
            # Tags from image
            for item in tweet.VisionResults.tags:
                if item.confidence > self.ms_confidence:
                    key = item.name
                    #costly to process the enter thing?
                    if tweetID not in self.index[key]:
                        self.index[key].insert(0,tweetID)

            # Captions from image
            for caption in tweet.VisionResults.description.captions:
                if caption.confidence > self.ms_confidence:
                    tokens = self.preprocesser.preprocess(caption.text)
                    for key in tokens:                    
                        if tweetID not in self.index[key]:      
                            self.index[key].insert(0, tweetID)


        if self.use_google and tweet.GoogleResults is not None:
            response = tweet.GoogleResults.responses[0]
            if hasattr(response, "labelAnnotations"):
                for item in response.labelAnnotations:
                    if item.score > self.google_confidence:
                        tokens = self.preprocesser.preprocess(item.description)
                        for key in tokens:
                            if tweetID not in self.index[key]:
                                self.index[key].insert(0,tweetID)

    def export(self):
        if self.fileService is None or self._tweet_count <= self._initial_tweet_count:
            return
        obj = {}
        obj['tweet_count'] = self._tweet_count
        obj['index'] = self.index
        self._initial_tweet_count = obj['tweet_count']
        if(self._tweet_count > 0):
            self.fileService.write(json.dumps(obj))

    
    def validate_confidence(self, propName, value):
        if value < 0.0 or value > 1.0:
            raise Exception("Value of {0} must be between 0 and 1.".format(propName))