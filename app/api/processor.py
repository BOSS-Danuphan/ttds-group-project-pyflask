import re, urllib
from nltk.stem import PorterStemmer
from app.utils import safeurlopen

class PreProcessor:
    _re_url = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:$%_\+.~#?&//=]*)')
    _re_usernames = re.compile("@\w+") # Twitter usernames
    _re_s_endings = re.compile("s\'s\\b") # "s's"
    _re_apostrophes = re.compile("'")
    _re_non_word_space = re.compile("[^\w\s]") # Non-word and non-white space

    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stopwords = self.load_stopwords()
        self.offensive = self.load_offensivewords()

    def stemming(self, terms):
        result = [self.stemmer.stem(term) for term in terms]
        return result

    def tokenize(self, content):
        if content is None:
            return []

        content = content.lower()
        content = self.remove_urls(content)
        content = self._re_usernames.sub("", content)
        content = self._re_s_endings.sub("s",content)
        content = self._re_apostrophes.sub("",content)
        content = self._re_non_word_space.sub(" ", content)
        content = content.split()
        return content

    def load_stopwords(self):
        stopwords = safeurlopen('http://members.unine.ch/jacques.savoy/clef/englishST.txt')
        stopwords = self.tokenize(stopwords)
        stopwords.append("rt")
        return stopwords

    def load_offensivewords(self):
        offensive_words = safeurlopen('http://www.bannedwordlist.com/lists/swearWords.txt')
        return self.tokenize(offensive_words)

    def remove_stopwords(self, terms):
        result = [term for term in terms if term not in self.stopwords]
        return result

    def remove_urls(self, text):
        return self._re_url.sub("", text)

    def preprocess(self, text):
        terms = self.tokenize(text)
        # Filter out potentially offensive tweets
        if any(term in self.offensive for term in terms):
            return []
        terms = self.remove_stopwords(terms)
        terms = self.stemming(terms)
        return terms
