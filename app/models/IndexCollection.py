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
                # TEST
                print('Adding: ', key)
                self.index[key] = [tweetID]
            else:
                self.index[key].append(tweetID)

        # TODO: Code appears to need refactored to work with the new models

        # TODO: index vision results etc.
        # tags
        # for tag in vision.tags:
        #     tag.confidence, tag.name
        # captions
        # for caption in vision.description.captions:
        #     caption.confidence, caption.text

        # """tags: cut above the confidence 50
        #     key of list of dictionaries with 'confidence' and 'name'"""

        #tags from image!
        # tweetID = tweetandvision['Tweet']['ID']
        # for item in tweetandvision['VisionResults']['tags']:
        #     if item['confidence']>0.5:
        #         key= item['name']
        #         #costly to process the entier thing?
        #         if key not in self.index:
        #             self.index[key] = [tweetID]
        #         else: #given each tweetID will be unique
        #             self.index[key].append(tweetID)

        # #caption from image!
        # caption = tweetandvision['VisionResults']['description']['captions'][0]['text']
        # for key in self.preprocesser.preprocess(caption):
        #     if key not in self.index:
        #         self.index[key] = [tweetID]
        #     else:
        #         self.index[key].append(tweetID)

    def export(self, target):
        '''Export in-memory index to a given file'''
        raise NotImplementedError