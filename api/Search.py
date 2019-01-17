from datetime import datetime
from storage import app_index_collection

class SearchModule(object):
    @staticmethod
    def search(query, limit=None):
        # Only example on how to call app_index_collection
        # isloaded = app_index_collection._loaded
        return {
            'total': 0,
            'data':[]
        }
