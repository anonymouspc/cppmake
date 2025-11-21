from cppmakelib.basic.config import config
from cppmakelib.error.config import ConfigError
import importlib

def import_file(file): ...



def import_file(file):
    try:
        module = importlib.machinery.SourceFileLoader(
            fullname=file.removesuffix(".py").replace('/', '.'), 
            path=file
        ).load_module()
    except FileNotFoundError:
        raise ConfigError(f"cppmake.py is not found (with path = {file})")
    return module
