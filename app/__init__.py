import os
from flask import Flask
import app.config

app = Flask(__name__, static_folder='../client/build')
app.config.from_object(os.environ.get('APP_SETTINGS', 'app.config.ProductionConfig'))
app.app_context().push()

if app.config.get('DEBUG'):
    from flask_cors import CORS
    cors = CORS(app)

from app.storage import app_index_collection
from app import routes

import atexit
def on_exit():
    """This method will run when application is being terminated."""
    print('Service being terminated: call on_exit !!')
    app_index_collection.export()
atexit.register(app_index_collection.export)
