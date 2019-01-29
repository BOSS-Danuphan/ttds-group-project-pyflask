from app import app
from app import storage

if __name__ == '__main__':
    try:
        app.run()
    finally:
        # Export index on app exit
        storage.app_index_collection.export()