import os
from config import Config
from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS', 'config.ProductionConfig'))

app.app_context().push()

from storage import app_index_collection
from api.Search import SearchModule

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

if __name__ == '__main__':
    app.run()
