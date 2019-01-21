import os
from config import Config
from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS', 'config.ProductionConfig'))

app.app_context().push()

from storage import app_index_collection
from api.Search import SearchModule

########################################
#         Background Streaming         #
########################################
from twitter.TwitterStreamListener import TwitterStreamListener
import tweepy
from threading import Thread, active_count
thread = None
stream = None

def backgroundthread():
    # TODO: Move to new separated file
    print('Background thread started')

    auth = tweepy.OAuthHandler(app.config.get('TWEEPY_CONSUMER_KEY'), app.config.get('TWEEPY_CONSUMER_SECRET'))
    auth.set_access_token(app.config.get('TWEEPY_ACCESS_TOKEN_KEY'), app.config.get('TWEEPY_ACCESS_TOKEN_SECRET'))
    api = tweepy.API(auth)

    streamListener = TwitterStreamListener(api)

    global stream
    stream = tweepy.Stream(auth = api.auth, listener=streamListener)
    stream.sample()
    print('Stream started')

class StoppableStreamThread(Thread):
    '''Inject streaming control'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def streamstop(self):
        stream.disconnect()
        print('Stream stopped')

    def streamstopped(self):
        return stream.running == False

###########################
#        Web Route        #
###########################
@app.route('/')
def hello_world():
    return render_template('article.html', content='Hello, World!')

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/api/search')
def apisearch():
    q = request.args.get('q')
    limit = request.args.get('limit')
    result = SearchModule.search(q, limit)
    return jsonify({
        **result,
        'ts': datetime.now().strftime(app.config['DATETIME_FORMAT']),
        'message': f'q is {q} and limit is {limit}'
    })

@app.route('/api/streamstatus')
def apistreamstatus():
    count = app_index_collection._count
    global thread
    return jsonify({
        'nThread': active_count(),
        'streamStatus': 'stopped' if thread is None or thread.streamstopped() else 'running',
        'ts': datetime.now().strftime(app.config['DATETIME_FORMAT']),
        'message': f'Collected {count} document(s) in total'
    })

@app.route('/api/streamstart')
# TODO: Allow only POST method
def twstreamstart():
    global thread
    if thread is None:
        thread = StoppableStreamThread(target=backgroundthread)
        thread.daemon = True
        thread.start()
    elif thread.streamstopped():
        thread = StoppableStreamThread(target=backgroundthread)
        thread.daemon = True
        thread.start()
    return jsonify({
        'message': 'Stream started !!'
    })

@app.route('/api/streamstop')
# TODO: Allow only POST method
def twstreamstop():
    global thread
    if thread is not None:
        thread.streamstop()
    return jsonify({
        'message': 'Stream stopped !!'
    })

if __name__ == '__main__':
    app.run()
