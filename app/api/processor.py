import re, urllib
from nltk.stem import PorterStemmer

class PreProcessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stopwords = self.load_stopwords()
    
    def stemming(self, terms):
        result = [self.stemmer.stem(term) for term in terms]
        return result

    def tokenize(self, content):
        content = content.lower()
        content = re.compile("s\'s\\b").sub("s",content)
        content = re.compile("'").sub("",content)
        content = re.compile("[^\w\s]").sub(" ", content)
        content = content.split()
        return content

    def load_stopwords(self):
        stop = urllib.request.urlopen('http://members.unine.ch/jacques.savoy/clef/englishST.txt') 
        stopwords = stop.read().decode('utf-8') 
        return self.tokenize(stopwords)
    
    def remove_stopwords(self, terms):
        result = [term for term in terms if term not in self.stopwords]
        return result

    def preprocess(self, text):
        terms = self.tokenize(text)
        terms = self.remove_stopwords(terms)
        terms = self.stemming(terms)
        return terms