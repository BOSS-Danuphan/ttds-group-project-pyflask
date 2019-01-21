class IndexCollection():
    '''This class aims to keep search index in memory'''
    _loaded=None
    _count=0

    def __init__(self, file):
        if file is not None:
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
