from cppmakelib.utility.decorator import member
import functools
import re
import typing

@functools.total_ordering
class Version:
    class ParseError(Exception):
        pattern : str
        string  : str
        position: int
    def __init__(self: Version, subversions: list[int])                    -> None   : ...
    def __str__ (self: Version)                                            -> str    : ...
    def __eq__  (self: Version, right: Version | typing.Any)               -> bool   : ...
    def __lt__  (self: Version, right: Version | int | float | typing.Any) -> bool   : ...
    @staticmethod
    def parse   (pattern: str, string: str)                                -> Version: ...
    sep        : str = '.'
    subversions: list[int]



@member(Version)
def __init__(self: Version, subversions: list[int]) -> None:
    self.subversions = subversions

@member(Version)
def __str__(self: Version) -> str:
    return Version.sep.join([str(subversion) for subversion in self.subversions])

@member(Version)
def __eq__(self: Version, right: Version | typing.Any) -> bool:
    if isinstance(right, Version):
        return self.subversions == right.subversions
    else:
        return NotImplemented
    
@member(Version)
def __lt__(self: Version, right: Version | int | float | typing.Any) -> bool:
    if isinstance(right, Version):
        return self.subversions < right.subversions
    elif isinstance(right, int):
        return self.subversions[0] < right
    elif isinstance(right, float):
        return self.subversions[0] <  int(right) or \
               self.subversions[0] == int(right) and self.subversions[1] < int(str(right).partition('.')[2])
    else:
        return NotImplemented
    
@member(Version)
def parse(pattern: str, string: str) -> Version:
    versions = re.findall(pattern=pattern, string=string)
    if len(versions) == 0:
        raise Version.ParseError(f'failed to parse version (with pattern = {pattern}, string = {string})')
    elif len(versions) == 1:
        return Version([int(subversion) for subversion in versions[0]])
    elif len(versions) >= 2:
        raise Version.ParseError(f'ambiguous version (with pattern = {pattern}, string = {string})')
    else:
        assert False
