from app.api.processor import PreProcessor
from app.twitter.AnalysedTweet import AnalysedTweet
from collections import defaultdict
import json, time

class TermCount():
    def __init__(self):
        self.vision_count = 0
        self.text_count = 0

class IndexCollection():
    '''This class aims to keep search index in memory'''
    _loaded=None
    _tweet_count=0
    _initial_tweet_count=0
    _export_frequency = 100

    def __init__(self, fileService=None, use_google=False, use_ms=False, google_confidence = 0.6, ms_confidence=0.6, use_stemming=True, use_stopping=True):
        self.index = {}
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
            self.index = dict(json_dict["index"])

        self._loaded = True

    def add_tweet(self, tweet):
        added_tweet = 0
        if (self._tweet_count % self._export_frequency == 0):
            self.export()

        tweetId = str(tweet.OriginalId  if tweet.OriginalId is not None else tweet.Id)

        term_counts = defaultdict(TermCount)

        # Index tweet text
        terms = self.preprocesser.preprocess(tweet.Text)
        if terms is None:
            # Preprocessor returns None if tweet contains offensive terms. Stop processing.
            return

        for term in terms:
            term_counts[term].text_count += 1
            
        if self.use_ms and tweet.VisionResults is not None:
            # Image Tags
            for tag in tweet.VisionResults.tags:
                if tag.confidence > self.ms_confidence:
                    term = tag.name
                    term_counts[term].vision_count += 1

            # Captions from image
            for caption in tweet.VisionResults.description.captions:
                if caption.confidence > self.ms_confidence:
                    terms = self.preprocesser.preprocess(caption.text)
                    for term in terms:                    
                        term_counts[term].vision_count += 1            

        if self.use_google and tweet.GoogleResults is not None:
            response = tweet.GoogleResults.responses[0]
            if hasattr(response, "labelAnnotations"):
                for label in response.labelAnnotations:
                    if label.score > self.google_confidence:
                        terms = self.preprocesser.preprocess(label.description)
                        for term in terms:
                            term_counts[term].vision_count += 1

        
            if hasattr(response, "logoAnnotations"):
                for logo in response.logoAnnotations:
                    if logo.score > self.google_confidence:
                        terms = self.preprocesser.preprocess(logo.description)
                        for term in terms:
                            term_counts[term].vision_count += 1

        for term, term_count in term_counts.items():
            if term_count.text_count == 0 and term_count.vision_count == 0:
                continue
            if term not in self.index:
                self.index[term] = {}
            if tweetId not in self.index[term]:
                self.index[term][tweetId] = [time.time(), 0, 0]
                added_tweet += 1
            
            self.index[term][tweetId][0] = time.time()
            self.index[term][tweetId][1] += term_count.text_count
            self.index[term][tweetId][2] += term_count.vision_count

        if added_tweet != 0:
            self._tweet_count += 1


    def export(self):
        if self.fileService is None or self._tweet_count <= self._initial_tweet_count:
            return
        obj = {}
        obj['tweet_count'] = self._tweet_count
        obj['index'] = self.index
        self._initial_tweet_count = self._tweet_count
        if(self._tweet_count > 0):
            self.fileService.write(json.dumps(obj))

    
    def validate_confidence(self, propName, value):
        if value < 0.0 or value > 1.0:
            raise Exception("Value of {0} must be between 0 and 1.".format(propName))