from cppmakelib.package.all        import context
from cppmakelib.utility.decorator  import member, pre, unique_in
from cppmakelib.utility.filesystem import get_file_modify_time, normal_path, path
from cppmakelib.utility.time       import time
import typing
if typing.TYPE_CHECKING:
    from cppmakelib.unit.header import Header

class Preparsed:
    def           __new__       (cls : type[Preparsed], file: path, from_header: Header) -> Preparsed: ...
    def           __init__      (self: Preparsed,       file: path, from_header: Header) -> None     : ...
    def             install     (self: Preparsed)                                        -> None     : ...
    async def async_install     (self: Preparsed)                                        -> None     : ...
    def             is_installed(self: Preparsed)                                        -> bool     : ...
    async def async_is_installed(self: Preparsed)                                        -> bool     : ...
    preparsed_file  : path
    install_file: path
    modify_time           : time
    from_header           : Header
    include_headers       : list[Preparsed]



@member(Preparsed)
@unique_in(context.package)
@pre(1, normal_path)
def __init__(self: Preparsed, file: path, from_header: Header) -> None:
    self.file        = file
    self.install_file = 
    self.from_header = from_header
    self.modify_time = get_file_modify_time(self.file)