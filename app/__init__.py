import os
from flask import Flask
import app.config

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS', 'app.config.ProductionConfig'))
app.app_context().push()

from app.storage import app_index_collection
from app import routes
