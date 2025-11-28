from cppmakelib.basic.exit        import on_terminate, rethrow_exception, current_exception
from cppmakelib.utility.color     import red, bold
from cppmakelib.utility.decorator import member
import sys

class LogicError(Exception):
    def __init__     (self, message): ...
    def __terminate__():              ...



@member(LogicError)
def __init__(self, message):
    self.args = [message]
    on_terminate(LogicError.__terminate__)

@member(LogicError)
def __terminate__():
    try:
        rethrow_exception(current_exception())
    except LogicError as error:
        print(f"{red(bold("fatal error:"))} {error}", file=sys.stderr)
