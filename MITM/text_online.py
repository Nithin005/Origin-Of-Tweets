from urllib.parse import urlencode
import requests
import json
import pprint
import re

from origin_finder.logger import logger
from origin_finder.Searx import SearxClient
from origin_finder.text.utils import calc_metric, extract_keywords
from fake_news import utils as fn_utils

# #inputs
# query = r'purple "best city" forest'
# keywords = ['purple', 'best city', 'forest']
query = ''
keywords = []

#load config
with open('config.json') as f:
    config = json.load(f)

def order_list_based_on(list, index):
    """
    sort based on a index

    Parameters:
    list (list): input list to be sorted
    index (int): name of the column to be sorted
    """
    list.sort(key=lambda x: x[index], reverse=True)

def pretty_str(str):
    """
    pretty format the string

    Parameters:
    str (str): Input text

    Returns:
    str: pretty formatted string
    """
    return pprint.pformat(str)

def main():
    #initializze SearxClient
    searx = SearxClient(config['searx_url'])
    engines = config['use_engines']

    results = []

    #iterate over engines and get results
    for engine_name in engines:
        global query
        req_params = {
            'engines': engine_name
        }
        res = searx.request(query, req_params)
        res = res['results']
        query = res['query']
        #append to global results
        results = results + res

    # logger.debug(pretty_str(results[0]))
    logger.debug(f'number of results: {len(results)}')

    results = post_process(results)

    #sort by metric
    order_list_based_on(results, 'metric')

    #export data to json
    with open('results.json', 'w') as f:
        json.dump(results, f)

    #print results
    _len = len(results) if len(results) < 10 else 10
    for i, result in enumerate(results[0:_len]):
        print(f"{i+1} | {result['engine']} | {result['title'].ljust(75)}... | {result['url']} | {result['pubdate']} | {result['veracity']}")

def post_process(results):
    #assigning the metric to each result
    query = results['query']
    keywords = query.replace('"', '').split()

    for result in results['results']:
        text = result['content']+result['title']
        timestamp = result['timestamp']
        print(keywords)
        metric =  calc_metric(keywords, text, timestamp)
        result['metric'] = metric

        _res = fn_utils.predict_one(text)
        result['veracity'] = _res
        result['keywords'] = extract_keywords(text)

    return results

if __name__ == '__main__':
    main()