from flask import Flask, render_template, jsonify, request, send_from_directory, safe_join
import os
from app import app
from datetime import datetime
from app.storage import app_index_collection, app_search

########################################
#         Background Streaming         #
########################################
from app.twitter.TwitterStreamListener import TwitterStreamListener
from app.twitter.TwitterStreamBuilder import TwitterStreamBuilder
import tweepy
from threading import Thread, active_count, Event
thread = None
stream = None

def backgroundthread():
    # TODO: Move to new separated file
    print('Background thread started')

    global stream
    stream = TwitterStreamBuilder.StreamBuilder()
    print('Stream started')
    stream.sample()

class StoppableStreamThread(Thread):
    '''Inject streaming control'''
    def __init__(self, *args, **kwargs):
        super(StoppableStreamThread, self).__init__(*args, **kwargs)
        self._stop = Event()

    def stop(self):
        if stream is not None:
            stream.disconnect()
        self._stop.set()
        print('Stream stopped')

    def stopped(self):
        return stream is None or stream.running == False

###########################
#        Web Route        #
###########################
@app.route('/', defaults={'filename': 'index.html'})
@app.route('/<path:filename>')
def servefile(filename):
    staticrootpath = "../client/build"
    try:
        return send_from_directory(staticrootpath, filename)
    except:
        return send_from_directory(staticrootpath, 'index.html')

@app.route('/static/<string:folder>/<path:filename>')
def servestatic(folder, filename):
    staticpath = os.path.join("../client/build/static", folder)
    print('static:', staticpath, filename)
    return send_from_directory(staticpath, filename)

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/api')
def apihome():
    return render_template('article.html', content='Hello, World!')

@app.route('/api/search')
def apisearch():
    """
    params:
        q: Search query
        limit: the number of results
    """
    q = request.args.get('q')
    limit = request.args.get('limit')
    if limit is not None and limit.isdigit():
        # if limit >= 0
        limit = int(limit)
    else:
        limit = None
    results = app_search.match(q, limit)

    return jsonify({
        'data': results,
        'ts': datetime.now().strftime(app.config['DATETIME_FORMAT']),
        'message': f'q is {q} and limit is {limit}'
    })

@app.route('/api/streamstatus')
def apistreamstatus():
    count = app_index_collection._tweet_count
    global thread
    return jsonify({
        'nThread': active_count(),
        'streamStatus': 'stopped' if thread is None or thread.stopped() else 'running',
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
    elif thread.stopped():
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
        thread.stop()
    return jsonify({
        'message': 'Stream stopped !!'
    })
