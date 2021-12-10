import requests
import json
from datetime import datetime

from origin_finder.logger import logger
from urllib.parse import urlencode

class TimestampConv():
    def __init__(self):
        pass

    def default(date_string):
        _dt = datetime.fromisoformat(date_string)
        return _dt.timestamp()

class SearxClient():
    def __init__(self, url):
        self.url = url
        pass

    def request(self, query, params):
        params['format'] = 'json'
        _url = self.url + f'/search?q={query}&' + urlencode(params)
        logger.debug(f'GET: {_url}')
        res = requests.get(_url)
        res = json.loads(res.text)
        self.add_timestamp(res['results'])
        return res

    def request_user(self, query, params):
        params['format'] = 'json'
        _url = self.url + f'/search/user?q={query}&' + urlencode(params)
        logger.debug(f'GET: {_url}')
        res = requests.get(_url)
        res = json.loads(res.text)
        return res

    def add_timestamp(self, results):
        for result in results:
            engine = result['engine']
            if(engine =='twitter'):
                result['timestamp'] = TimestampConv.default(result['pubdate'])
            if(engine == 'reddit'):
                result['timestamp'] = TimestampConv.default(result['pubdate'])