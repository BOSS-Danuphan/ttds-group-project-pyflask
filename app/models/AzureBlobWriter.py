import io, time
from app import app
from azure.storage.blob import BlockBlobService, PublicAccess

class AzureBlobWriter:
    
    def __init__(self, file_path="index.txt"):
        # Create a new file on every instantiation
        epoch_time = str(time.time()).split('.')[0]
        self.file_path = "{0}-{1}".format(file_path, epoch_time)
        self.blob_service = BlockBlobService(account_name=app.config['AZURE_BLOB_ACCOUNT'], account_key=app.config['AZURE_BLOB_KEY'])
        self.container_name = "ttds-indexes"

    def read(self):
        try:
            # Get the most recently written file with the specified name
            highest_blob = 0
            blob_name = self.file_path

            container = self.blob_service.list_blobs(self.container_name)
            for blob in container:
                blob_order = int(blob.name.split("-")[1])
                if blob_order > highest_blob:
                    highest_blob = blob_order
                    blob_name = blob.name

            blob = self.blob_service.get_blob_to_text(self.container_name, blob_name)
            return blob.content
        except:
            return None

    def write(self, content):
        self.blob_service.create_blob_from_text(self.container_name, self.file_path, content)