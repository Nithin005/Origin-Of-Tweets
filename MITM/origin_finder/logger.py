import logging

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('--- %(module)s : %(levelname)s : %(message)s')
console.setFormatter(formatter)

logger = logging.getLogger('searx')
logger.setLevel(logging.DEBUG)
logger.addHandler(console)
