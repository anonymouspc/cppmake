from cppmakelib.package.all        import context
from cppmakelib.utility.decorator  import member, pre, unique_in
from cppmakelib.utility.filesystem import get_file_modify_time, normal_path, path
from cppmakelib.utility.time       import time
import typing
if typing.TYPE_CHECKING:
    from cppmakelib.unit.module import Module

class Precompiled:
    def           __new__       (cls : type[Precompiled], file: path, from_module: Module) -> Precompiled: ...
    def           __init__      (self: Precompiled,       file: path, from_module: Module) -> None       : ...
    def             install     (self: Precompiled)                                        -> None       : ...
    async def async_install     (self: Precompiled)                                        -> None       : ...
    def             is_installed(self: Precompiled)                                        -> bool       : ...
    async def async_is_installed(self: Precompiled)                                        -> bool       : ...
    file           : path
    install_file   : path
    modify_time    : time
    from_module    : Module
    include_headers: list[Precompiled]



@member(Precompiled)
@unique_in(context.package)
@pre(1, normal_path)
def __init__(self: Precompiled, file: path, from_module: Module) -> None:
    self.file        = file
    self.from_module = from_module
    self.modify_time = get_file_modify_time(self.file)