import re, urllib
from nltk.stem import PorterStemmer

class PreProcessor:
    def __init__(self):
        self.stem = PorterStemmer()
        self.stopwords = self.listtostop()
    
    def stemming(self,term):
        return self.stem.stem(term)

    def tokenize(self,content):
        content = content.lower()
        content = re.compile("s\'s\\b").sub("s",content)
        content = re.compile("'").sub("",content)
        content = re.compile("[^\W\s]").sub(" ", content)
        content = content.split()
        return content

    def listtostop(self):
        stop = urllib.request.urlopen('http://members.unine.ch/jacques.savoy/clef/englishST.txt') 
        stopwords = stop.read().decode('utf-8') 
        return self.tokenize(stopwords)
    
    def rid_stopwords(self, word):
        if word in self.stopwords:
            return False
        return True

    def preprocess(self, text):
        terms = self.tokenize(text)
        terms = self.rid_stopwords(terms)
        terms = self.stemming(terms)
        return terms