import io, time
from app import app
import sys
from datetime import datetime
from azure.storage.blob import BlockBlobService, PublicAccess
from app.utils import sizeof_fmt

class AzureBlobWriter:

    def __init__(self, file_path="index.txt"):
        # Create a new file on every instantiation
        epoch_time = str(time.time()).split('.')[0]
        self._file_path = "{0}-{1}".format(file_path, epoch_time)
        self._blob_service = BlockBlobService(account_name=app.config['AZURE_BLOB_ACCOUNT'], account_key=app.config['AZURE_BLOB_KEY'])
        self._container_name = "ttds-indexes"

    def read(self):
        content = None
        try:
            # Get the most recently written file with the specified name
            highest_blob = 0
            blob_to_load = ""
            blob_name = self._file_path.rsplit("-", 1)[0]
            blob_found = False

            container = self._blob_service.list_blobs(self._container_name)
            for blob in container:
                name_parts = blob.name.rsplit("-", 1)
                blob_prefix = name_parts[0]
                blob_order = int(name_parts[1])
                if blob_prefix == blob_name and blob_order > highest_blob:
                    highest_blob = blob_order
                    blob_to_load = blob.name
                    blob_found = True

            if blob_found:
                blob = self._blob_service.get_blob_to_text(self._container_name, blob_to_load)
                content = blob.content
        except:
            print("Unexpected error at {}.read: {}".format(__name__, sys.exc_info()))
        else:
            print("Read content from {} by {} at {}".format(self._file_path, __name__, datetime.now().strftime(app.config['DATETIME_FORMAT'])))
        return content

    def write(self, content):
        try:
            self._blob_service.create_blob_from_text(self._container_name, self._file_path, content)
        except:
            print("Unexpected error at {}.write: {}".format(__name__, sys.exc_info()))
        else:
            print("Content of size {} has been written to {} by {} at {}".format(sizeof_fmt(content), self._file_path, __name__, datetime.now().strftime(app.config['DATETIME_FORMAT'])))
