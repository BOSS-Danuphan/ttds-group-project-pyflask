import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'This-is-secret!#$')
    DATETIME_FORMAT = os.environ.get('DATETIME_FORMAT', "%Y-%m-%d %H:%M:%S")
    INDEXFILE_PATH = os.environ.get("INDEXFILE_PATH", "myindex.txt")
    INDEX_WRITER = os.environ.get('INDEX_WRITER', '')
    
    TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
    TWITTER_ACCESS_TOKEN_KEY = os.environ.get('TWITTER_ACCESS_TOKEN_KEY')
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    MS_VISION_KEY = os.environ.get('MS_VISION_KEY')
    AZURE_BLOB_ACCOUNT = os.environ.get('AZURE_BLOB_ACCOUNT')
    AZURE_BLOB_KEY = os.environ.get('AZURE_BLOB_KEY')

    


class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
