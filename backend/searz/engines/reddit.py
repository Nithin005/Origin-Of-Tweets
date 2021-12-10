# SPDX-License-Identifier: AGPL-3.0-or-later
"""
 Reddit
"""

import json
from datetime import datetime
from urllib.parse import urlencode, urljoin, urlparse

# about
about = {
    "website": 'https://www.reddit.com/',
    "wikidata_id": 'Q1136',
    "official_api_documentation": 'https://www.reddit.com/dev/api',
    "use_official_api": True,
    "require_api_key": False,
    "results": 'JSON',
}

# engine dependent config
categories = ['general', 'images', 'news', 'social media']
page_size = 25

# search-url
base_url = 'https://www.reddit.com/'
search_url = base_url + 'search.json?{query}'


# do search-request
def request(query, params):
    query = urlencode({'q': query, 'limit': page_size})
    params['url'] = search_url.format(query=query)

    return params


# get response from search-request
def response(resp):
    text_results = []

    search_results = json.loads(resp.text)

    # return empty array if there are no results
    if 'data' not in search_results:
        return []

    posts = search_results.get('data', {}).get('children', [])

    # process results
    for post in posts:
        data = post['data']

        # extract post information
        params = {
            'url': urljoin(base_url, data['permalink']),
            'title': data['title']
        }

        created = datetime.fromtimestamp(data['created_utc'])
        params['publishedDate'] = created
        # if thumbnail field contains a valid URL, we need to change template
        thumbnail = data['thumbnail']
        url_info = urlparse(thumbnail)
        # netloc & path
        if url_info[1] != '' and url_info[2] != '':
            params['img_src'] = data['url']
            params['thumbnail_src'] = thumbnail

        content = data['selftext']
        if len(content) > 500:
            content = content[:500] + '...'
        params['content'] = content
        params['author'] = data['author']
        text_results.append(params)

    # show images first and text results second
    return text_results

def new(params):
    url = base_url + 'r/news/new.json'
    params['url'] = url
    return params

def user(id, params):
    url = base_url + f'user/{id}/about.json'
    params['url'] = url
    return params

def user_response(resp):
    result = json.loads(resp.text)
    return result['data']