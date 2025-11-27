from cppmakelib.error.config      import ConfigError
from cppmakelib.utility.decorator import member
import os
import sys

class Windows:
    name              = "windows"
    executable_suffix = ".exe"
    static_suffix     = ".lib"
    shared_suffix     = ".dll"
    compiler_path     = "cl.exe"
    env               = os.environ
    def __init__(self): ...



@member(Windows)
def __init__(self):
    self._check()

@member(Windows)
def _check(self):
    if sys.platform != "win32":
        raise ConfigError(f"system is not windows (with sys.platform = {sys.platform})")