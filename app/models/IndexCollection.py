from app.api.processor import PreProcessor
from app.twitter.AnalysedTweet import AnalysedTweet

class IndexCollection():
    '''This class aims to keep search index in memory'''
    _loaded=None
    _count=0

    def __init__(self):
        self.index ={}
        self.preprocesser = PreProcessor()
        

    def load(self, file=None):
        '''Reload index data from external source'''
        self._loaded = True
        self._count = 0
        raise NotImplementedError

    def add_tweet(self, tweet):
        self._count += 1
        
        tweetID = tweet.Id
        # Index tweet text
        for key in self.preprocesser.preprocess(tweet.Text):
            if key not in self.index:
                self.index[key] = [tweetID]
            else:
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
                if key not in self.index:
                    self.index[key] = [tweetID]
                else: #given each tweetID will be unique
                    self.index[key].append(tweetID)

        #caption from image!
        for caption in tweet.VisionResults.description.captions:
            if caption.confidence > 0.5:
                tokens = self.preprocesser.preprocess(caption.text)
                for key in tokens:
                    if key not in self.index:
                        self.index[key] = [tweetID]
                    else:
                        self.index[key].append(tweetID)

    def export(self, target):
        '''Export in-memory index to a given file'''
        raise NotImplementedError