from cppmakelib.error.config       import ConfigError
from cppmakelib.utility.decorator  import member
from cppmakelib.utility.filesystem import path, resolvable_path
import sys

class Linux:
    def __init__(self: Linux) -> None: ...
    executable_suffix: str             = ''
    object_suffix    : str             = 'o'
    static_suffix    : str             = 'a'
    dynamic_suffix   : str             = 'so'
    compiler         : resolvable_path = 'g++'
    install_dir      : path            = '/usr'

    def _check(self: Linux) -> None: ...



@member(Linux)
def __init__(self: Linux) -> None:
    self._check()

@member(Linux)
def _check(self: Linux) -> None:
    if sys.platform != 'linux':
        raise ConfigError(f'linux check failed (with sys.platform = {sys.platform})')