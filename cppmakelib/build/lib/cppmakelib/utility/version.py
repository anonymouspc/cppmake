from cppmakelib.error.logic    import LogicError
from cppmakelib.utility.inline import assert_
import functools
import re

def parse_version(version_str): ...


def parse_version(version_str):
    try:
        return _Version([int(num) for num in re.search(r'\b\d+(?:\.\d+)+\b', version_str).group().split('.')])
    except:
        raise LogicError(f"version parse failed (with version_str = {version_str})")

@functools.total_ordering
class _Version:
    def __init__(self, ver):
        self._ver = ver

    def __getitem__(self, index):
        return self._ver[index]
    
    def __str__(self):
        return '.'.join([str(num) for num in self._ver])
    
    def __eq__(self, ver):
        if type(ver) == int:
            return self._ver[0] == ver
        elif type(ver) == float:
            return self._ver[0] == int(ver) and \
                   self._ver[1] == int(str(ver).split('.')[2])
        elif type(ver) == _Version:
            return self._ver == ver._ver
        else:
            return NotImplemented
        
    def __lt__(self, ver):
        if type(ver) == int:
            return self._ver[0] < ver
        elif type(ver) == float:
            return self._ver[0] <  int(ver) or \
                   self._ver[0] == int(ver) and self._ver[1] < int(str(ver).split('.')[2])
        elif type(ver) == _Version:
            return self._ver < ver._ver
        else:
            return NotImplemented