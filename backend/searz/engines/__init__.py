import sys
from os.path import realpath,dirname

from searz import utils

engine_dir = dirname(realpath(__file__))

def load_engine(engine_data):
    engine_name = engine_data['name']
    try:
        engine = utils.load_module(engine_name+'.py', engine_dir)
    except:
        print('engine not found')
        sys.exit(1)
    return engine
