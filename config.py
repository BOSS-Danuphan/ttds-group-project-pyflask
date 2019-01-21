import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'This-is-secret!#$')
    DATETIME_FORMAT = os.environ.get('DATETIME_FORMAT', "%Y-%m-%d %H:%M:%S")
    INDEXFILE_PATH = os.environ.get("myindex.txt", "myindex.txt")

    TWEEPY_CONSUMER_KEY = os.environ.get('TWEEPY_CONSUMER_KEY', 'consumer-key-here')
    TWEEPY_CONSUMER_SECRET = os.environ.get('TWEEPY_CONSUMER_SECRET', 'consumer-secret-here')
    TWEEPY_ACCESS_TOKEN_KEY = os.environ.get('TWEEPY_ACCESS_TOKEN_KEY', 'access-token-key-here')
    TWEEPY_ACCESS_TOKEN_SECRET = os.environ.get('TWEEPY_ACCESS_TOKEN_SECRET', 'access-token-secret-here')

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
