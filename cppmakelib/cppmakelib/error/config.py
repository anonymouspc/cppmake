from cppmakelib.basic.exit        import on_terminate, rethrow_exception, current_exception
from cppmakelib.utility.color     import red, bold
from cppmakelib.utility.decorator import member
import sys

class ConfigError(Exception):
    def __init__     (self, message): ...
    def __terminate__():              ...



@member(ConfigError)
def __init__(self, message):
    self.args = [message]
    on_terminate(ConfigError.__terminate__)

@member(ConfigError)
def __terminate__():
    try:
        rethrow_exception(current_exception())
    except ConfigError as error:
        print(f"{red(bold("fatal error:"))} {error}", file=sys.stderr)
