from app.models.IndexCollection import IndexCollection
from app.api.Search import SearchEngine
from app.twitter.AnalysedTweet import AnalysedTweet
from app.evaluation.EvalResult import EvalResult
import math

class IndexBuilder():
    
    def __init__(self):
        self.index = IndexCollection()
                
    def load(self, resultTuples):
        for result in resultTuples:
            tweet = self.buildTweetModel(result[0], result[1])
            self.index.add_tweet(tweet)

        return self.index

    def buildTweetModel(self, tweetJson, visionVson):
        tweet = AnalysedTweet()
        
        ### TODO: Re-use code from the Twitter model to build Analysed Tweet object
        return tweet