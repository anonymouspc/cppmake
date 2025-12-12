from cppmakelib.basic.exit        import on_terminate, rethrow_exception, current_exception
from cppmakelib.utility.decorator import member
import sys

class SubprocessError(Exception):
    def __init__     (self, stderr, is_stderr_printed, code): ...
    def __terminate__():                                      ...
    def __str__      (self):                                  ...



@member(SubprocessError)
def __init__(self, stderr, is_stderr_printed, code):
    self.args              = [stderr, is_stderr_printed, code]
    self.stderr            = stderr
    self.is_stderr_printed = is_stderr_printed
    self.code              = code
    on_terminate(SubprocessError.__terminate__)

@member(SubprocessError)
def __terminate__():
    try:
        rethrow_exception(current_exception())
    except SubprocessError as error:
        if not error.is_stderr_printed:
            print(error.stderr, file=sys.stderr)


@member(SubprocessError)
def __str__(self):
    return self.stderr