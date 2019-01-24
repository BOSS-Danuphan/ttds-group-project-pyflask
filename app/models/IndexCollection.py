from app.api.processor import PreProcessor
from app.twitter.AnalysedTweet import AnalysedTweet

class IndexCollection2():
    '''This class aims to keep search index in memory'''
    _loaded=None
    _count=0

    def __init__(self):
        self.load()

    def load(self, file=None):
        '''Reload index data from external source'''
        self._loaded = True
        self._count = 0

    def adddocument(self, document):
        '''update index with new document'''
        self._count += 1

    def export(self, target):
        '''Export in-memory index to a given file'''
        pass

class IndexCollection():
    """inverted index based on words from caption,tags from API + text"""
    def __init__(self):
        self.iid ={}
        self.preprocesser = PreProcessor()

    def load(self, instance):
        return instance

    def add_tweet(self, atweet):
        tweetID = atweet.Id
        # Index tweet text
        for key in self.preprocesser.preprocess(atweet.text):
            if key not in self.iid:
                self.iid[key] = [tweetID]
            else:
                self.iid[key] = [tweetID]
        # TODO: index vision results etc.
        # tags
        # for tag in vision.tags:
        #     tag.confidence, tag.name
        # captions
        # for caption in vision.description.captions:
        #     caption.confidence, caption.text
        

    def collect_label(self, tweetandvision):
        """tags: cut above the confidence 50
            key of list of dictionaries with 'confidence' and 'name'"""

        #tags from image!
        tweetID = tweetandvision['Tweet']['ID']
        for item in tweetandvision['VisionResults']['tags']:
            if item['confidence']>0.5:
                key= item['name']
                #costly to process the entier thing?
                if key not in self.iid:
                    self.iid[key] = [tweetID]
                else: #given each tweetID will be unique
                    self.iid[key].append(tweetID)

        #caption from image!
        caption = tweetandvision['VisionResults']['description']['captions'][0]['text']
        for key in self.preprocesser.preprocess(caption):
            if key not in self.iid:
                self.iid[key] = [tweetID]
            else:
                self.iid[key].append(tweetID)

        #text!
        tweettext = tweetandvision['Tweet']['Text']
        for key in self.preprocesser.preprocess(tweettext):
            if key not in self.iid:
                self.iid[key] = [tweetID]
            else:
                self.iid[key] = [tweetID]

    def main(self, direc):
        #given multiple files in direc
        ds = self.load('temp')
        self.collect_label(ds)
            
    def update(self, _tweets):
        #self.iid
        #how to get realtime tweets

        new_ds = self.load(_tweets)
        self.collect_label(new_ds)

    def export(self):
        return self.iid


if __name__ == '__main__':
    directory ='typein_repo_address'
    db = IndexCollection()
    db.main(directory)
    print(db.iid)
#to send to in-memory DB, fill in the git connected to Heroku
