class AnalysedTweet:    
    def __init__(self, tid=None, text=None, url=None, imageUrl=None, hashTags=[], vresults=None, gresults=None):
        self.Id = tid
        self.Text = text
        self.Url = url
        self.ImageUrl = imageUrl
        self.Hashtags = hashTags
        self.VisionResults = vresults
        self.GoogleResults = gresults
        return


