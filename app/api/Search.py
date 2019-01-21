from app.storage import app_index_collection

class SearchModule(object):
    @staticmethod
    def search(query, limit=None):
        '''Perform search in index by a given query'''
        # Only example on how to call app_index_collection
        # isloaded = app_index_collection._loaded
        return {
            'nDocucment': app_index_collection._count, # Example
            'total': 0,
            'data': []
        }

    @staticmethod
    def searchsingle(document, query):
        '''Perform search by given document and query'''
        return {
            'isRelevant': True, # Is this document relevant acording to a given query
            'document': document
        }
