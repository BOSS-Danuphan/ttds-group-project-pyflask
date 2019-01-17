class IndexCollection():
    '''This class aims to keep search index in memory'''
    _filepath=None
    _loaded=None
    def __init__(self, file):
        if file is not None:
            self.setfilepath(file)
            self.load()
    def setfilepath(self, file):
        self._filepath = file
    def load(self, file=None):
        '''Reload index data from a specific file'''
        if file is None:
            file = self._filepath
        self._loaded = True
    def export(self, target):
        '''Export in-memory index to a given file'''
        pass
