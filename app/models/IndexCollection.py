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

    def __init__(self, fileService=None):
        self.index = defaultdict(list)
        self.preprocesser = PreProcessor()
        self.fileService = fileService
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

        tweetID = tweet.Id
        # Index tweet text
        for key in self.preprocesser.preprocess(tweet.Text):
            self.index[key].append(tweetID)

        if tweet.VisionResults is None:
            return

        """tags: cut above the confidence 50
            key of list of dictionaries with 'confidence' and 'name'"""
        #tags from image!
        for item in tweet.VisionResults.tags:
            if item.confidence > 0.5:
                key = item.name
                #costly to process the enter thing?
                self.index[key].append(tweetID)

        #caption from image!
        for caption in tweet.VisionResults.description.captions:
            if caption.confidence > 0.5:
                tokens = self.preprocesser.preprocess(caption.text)
                for key in tokens:
                    self.index[key].append(tweetID)

    def export(self):
        if self.fileService is None or self._tweet_count <= self._initial_tweet_count:
            return
        obj = {}
        obj['tweet_count'] = self._tweet_count
        obj['index'] = self.index
        self._initial_tweet_count = obj['tweet_count']
        if(self._tweet_count > 0):
            self.fileService.write(json.dumps(obj))
