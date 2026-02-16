from cppmakelib.utility.decorator import implement

def red       (string: str) -> str: ...
 #  orange    (string: str) -> str: ...
def yellow    (string: str) -> str: ...
def green     (string: str) -> str: ...
def blue      (string: str) -> str: ...
def purple    (string: str) -> str: ...
def white     (string: str) -> str: ...
def gray      (string: str) -> str: ...
def black     (string: str) -> str: ...
def bold      (string: str) -> str: ...
def faint     (string: str) -> str: ...
def italicized(string: str) -> str: ...
def underlined(string: str) -> str: ...



@implement
def red(string: str) -> str:
    return f'\033[31m{string}\033[39m'

@implement
def yellow(string: str) -> str:
    return f'\033[33m{string}\033[39m'

@implement
def green(string: str) -> str:
    return f'\033[32m{string}\033[39m'

@implement
def blue(string: str) -> str:
    return f'\033[34m{string}\033[39m'

@implement
def purple(string: str) -> str:
    return f'\033[35m{string}\033[39m'

@implement
def white(string: str) -> str:
    return f'\033[37m{string}\033[39m'

@implement
def gray(string: str) -> str:
    return f'\033[90m{string}\033[39m'

@implement
def black(string: str) -> str:
    return f'\033[30m{string}\033[39m'

@implement
def bold(string: str) -> str:
    return f'\033[1m{string}\033[22m'

@implement
def faint(string: str) -> str:
    return f'\033[2m{string}\033[22m'

@implement
def italicized(string: str) -> str:
    return f'\033[3m{string}\033[23m'

@implement
def underlined(string: str) -> str:
    return f'\033[4m{string}\033[24m'