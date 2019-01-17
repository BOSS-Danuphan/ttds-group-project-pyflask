from models.IndexCollection import IndexCollection
from flask import current_app
app_index_collection = IndexCollection(current_app.config.get('INDEXFILE_PATH'))
