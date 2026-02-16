from cppmakelib.basic.context      import context
from cppmakelib.package.basic      import Package
from cppmakelib.utility.decorator  import member, pre, unique_in
from cppmakelib.utility.filesystem import get_file_modify_time, normal_path, path
from cppmakelib.utility.time       import time

class Binary:
    def           __new__  (cls : type[Binary], file: path) -> Binary: ...
    def           __init__ (self: Binary,       file: path) -> None  : ...
    def             install(self: Binary)                   -> None  : ...
    async def async_install(self: Binary)                   -> None  : ...
    file           : path
    modify_time    : time
    context_package: Package
    link_flags     : list[str]



@member(Binary)
@unique_in(context.package)
@pre(1, normal_path)
def __init__(self: Binary, file: path) -> None:
    self.file            = file
    self.modify_time     = get_file_modify_time(self.file)
    self.context_package = context.package
    self.link_flags      = self.context_package.link_flags