import sys
import importlib
from os.path import splitext, join


def load_module(filename, module_dir):
    modname = splitext(filename)[0]
    if modname in sys.modules:
        del sys.modules[modname]
    filepath = join(module_dir, filename)
    # and https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    spec = importlib.util.spec_from_file_location(modname, filepath)
    module = importlib.util.module_from_spec(spec)
    sys.modules[modname] = module
    spec.loader.exec_module(module)
    return module