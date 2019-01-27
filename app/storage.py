from app.models.IndexCollection import IndexCollection
from app.models.FileWriter import FileWriter
from app.api.Search import SearchEngine
from app import app

# Create an index writer of the specified type, if configured:
writer_type = app.config['INDEX_WRITER']
index_file = app.config['INDEXFILE_PATH']
writer = None
if writer_type:
    module = __import__('app.models.'+writer_type, fromlist=[writer_type])
    writerClass = getattr(module, writer_type)
    writer = writerClass(index_file)

app_index_collection = IndexCollection(writer)
app_search = SearchEngine(app_index_collection)
