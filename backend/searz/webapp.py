import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import searz.search.searcher as searcher
from searz.logger import logger

logger.info("server searz is starting...")

server = searcher.app

if __name__ == '__main__':
    searcher.app.run(port = 5001)


# query = 'purple "best city" forest'
# params = { 'query': query }
# engine_data = {'name': 'twitter'}

# res = searcher.search(params, engine_data)
# print(res)