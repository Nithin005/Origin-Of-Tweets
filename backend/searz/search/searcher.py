import requests
import json
import os.path
from searz.logger import logger
import searz.engines as engines
import flask
from flask import Flask, request
from datetime import datetime
import datetime as dt

with open(os.path.dirname(__file__) + '/../settings.json', 'r') as f:
    config = json.load(f)

def get_params(raw_params):
    params = {
        'q': None,
        'url': None,
        'headers': {
            'User-Agent': config['defaults']['search']['headers']
        },
        'stream': None
    }
    params.update(raw_params)
    return params

def get_engine_data(raw_params):
    engine_data = {
        'name': raw_params.get('engines', config['defaults']['search']['engine']),
    }
    return engine_data

def search(params, engine_data):
    engine = engines.load_engine(engine_data)
    rparams = engine.request(params['q'], params)

    res = requests.get(rparams['url'], headers = rparams.get('headers', {}))
    return engine.response(res)

def stream(params, engine_data):
    engine = engines.load_engine(engine_data)
    rparams = engine.new(params)
    print(rparams)
    res = requests.get(rparams['url'], headers = rparams.get('headers', {}))
    return engine.response(res)

def user_search(params, engine_data):
    engine = engines.load_engine(engine_data)
    rparams = engine.user(params['q'], params)
    print(rparams)
    res = requests.get(rparams['url'], headers = rparams.get('headers', {}))
    return engine.user_response(res)


def post_process(results, params, engine_data):
    for result in results:
        result['engine'] = engine_data['name']
        if(isinstance(result['publishedDate'], dt.date)):
            result['pubdate'] = result['publishedDate'].strftime('%Y-%m-%d %H:%M:%S%z')
            result['publishedDate'] = result['publishedDate'].strftime('%Y-%m-%d')
            

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def _search():
    print('hello')
    raw_params = flask.request.args.to_dict()
    params = get_params(raw_params)
    engine_data = get_engine_data(raw_params)
    res = []
    print(params)
    if(params['q']):
        res = search(params, engine_data)
    elif(params['stream']):
        res = stream(params, engine_data)
    post_process(res, params, engine_data)
    logger.debug(f'parsed response: {res}')
    return flask.jsonify({'results': res, 'query': params['q']})

@app.route('/search/user', methods=['GET'])
def _user_search():
    raw_params = flask.request.args.to_dict()
    params = get_params(raw_params)
    engine_data = get_engine_data(raw_params)
    res = user_search(params, engine_data)
    return flask.jsonify(res)
    

@app.after_request # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response