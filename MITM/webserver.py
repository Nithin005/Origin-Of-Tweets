import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from flask import Flask, render_template, request
from requests.api import post
from origin_finder.Searx import SearxClient
from text_online import post_process
import flask
from origin_finder.text.utils import extract_keywords

app = Flask(__name__)
searx = SearxClient('http://127.0.0.1:5001')


def parse_params(request):
    params = request.args.to_dict()
    print(params)
    query = params.get('q', '')
    if(query != ''):
        del params['q']
    return [query, params]


@app.route("/search")
def search():
    # params = request.args.to_dict()
    # print(params)
    # query = params.get('q', '')
    # if(query != ''):
    #     del params['q']
    
    # res = searx.request(query, params)
    query, params = parse_params(request)
    res = searx.request(query, params)
    res['query'] = query
    post_process(res)
    return flask.jsonify(res)

@app.route("/search/user")
def search_user():
    query, params = parse_params(request)
    params['path'] = '/search/user'
    res =  searx.request_user(query, params)
    return flask.jsonify(res)

@app.after_request # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

server = app

if __name__ == '__main__':
    app.run(port= 5002)