from datetime import datetime
from storage import app_index_collection

class SearchModule(object):
    @staticmethod
    def search(query, limit=None):
        return {
            'count': 0,
            'tids':[],
            'indexloaded': app_index_collection._loaded # Only example on how to call it
        }
