from cppmakelib.error.config      import ConfigError
from cppmakelib.utility.decorator import member
import os
import sys

class Macos:
    name              = "macos"
    executable_suffix = ""
    static_suffix     = ".a"
    shared_suffix     = ".dylib"
    compiler_path     = "clang++"
    env               = os.environ
    def __init__(self): ...



@member(Macos)
def __init__(self):
    self._check()

@member(Macos)
def _check(self):
    if sys.platform != "darwin":
        raise ConfigError(f"system is not macos (with sys.platform = {sys.platform})")