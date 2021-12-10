# SPDX-License-Identifier: AGPL-3.0-or-later
import json
from urllib.parse import urlencode

from datetime import datetime
from searz.logger import logger

"""
 Twitter
"""

# about
about = {
    "website": 'https://twitter.com/',
    "wikidata_id": None,
    "official_api_documentation": None,
    "use_official_api": True,
    "require_api_key": True,
    "results": 'JSON',
}

# engine dependent config
categories = ['general']
paging = True

# config
MAX_RESULTS = 100
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAGU3UAEAAAAAWPU9vUxvRqZGhIPJK4FPmC6nJz4%3DSDjqPjP6hzLIXKiCLN3QgMK6pTl5qBQH10072WvhEPdejoyXU2'

base_url = 'https://api.twitter.com/'

# do search-request
def _request(base, query, params):
    qstring = {
        'max_results':  MAX_RESULTS,
        'tweet.fields': 'author_id,created_at',
        'expansions' : 'author_id',
        'user.fields': 'name,username,created_at'
    }
    headers = {}
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    # params['url'] = r'{}'.format(base_url + search_url.format(query=f'q={query}&'+urlencode(qstring)))
    params['url'] = f'{base_url}{base}?query={query}&{urlencode(qstring)}'
    params['headers'] = headers
    logger.debug(f'params: {params}')
    return params

def request(query, params):
    return _request('2/tweets/search/recent', query, params)


# get response from search-request
def response(resp):
    logger.debug(f'response: {resp.text}')
    results = []

    search_results = json.loads(resp.text)

    # if 'data' not in search_results:
    #     return []

    tweets = search_results.get('data', [])
    _users = search_results.get('includes', {}).get('users', [])
    users = {}
    for _user in _users:
        users[_user['id']] = _user

    for tweet in tweets:
        params = {
            'author': users[tweet['author_id']]['username'],
            'id': tweet['id'],
            'content': tweet['text']
        }
        params['title'] = tweet['text']
        date_string = tweet['created_at'][0:-1]
        created = datetime.fromisoformat(date_string)
        params['publishedDate'] = created
        params['url'] = 'https://twitter.com/twitter/status/'+tweet['id']
        results.append(params)
    return results

def new(params):
    qstring = {
        'tweet.fields': 'author_id,created_at',
        'expansions' : 'author_id',
        'user.fields': 'name,username,created_at'
    }
    headers = {}
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    # params['url'] = r'{}'.format(base_url + search_url.format(query=f'q={query}&'+urlencode(qstring)))
    params['url'] = f'{base_url}2/tweets/sample/stream?{urlencode(qstring)}'
    params['headers'] = headers
    logger.debug(f'params: {params}')
    return params

def user(id, params):
    qstring = {
        'user.fields': 'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld'
    }
    headers = {}
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    # params['url'] = r'{}'.format(base_url + search_url.format(query=f'q={query}&'+urlencode(qstring)))
    params['url'] = f'{base_url}2/users/by/username/{id}?{urlencode(qstring)}'
    params['headers'] = headers
    logger.debug(f'params: {params}')
    return params

def user_response(resp):
    result = json.loads(resp.text)
    print(result)
    return result['data']
