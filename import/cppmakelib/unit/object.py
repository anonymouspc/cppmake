from cppmakelib.compiler.all       import compiler
from cppmakelib.executor.scheduler import scheduler
from cppmakelib.system.all         import system
from cppmakelib.unit.binary        import Binary
from cppmakelib.unit.dynamic       import Dynamic
from cppmakelib.unit.executable    import Executable
from cppmakelib.utility.algorithm  import recursive_collect
from cppmakelib.utility.decorator  import member, once, syncable
from cppmakelib.utility.filesystem import iterate_dir, path, replace_suffix_file
import typing
if typing.TYPE_CHECKING:
    from cppmakelib.unit.module import Module
    from cppmakelib.unit.source import Source

class Object(Binary):
    def           __init__   (self, file: path, from_code: Module | Source) -> None      : ...
    def             share    (self)                                         -> Dynamic   : ...
    async def async_share    (self)                                         -> Dynamic   : ...
    def             is_shared(self)                                         -> bool      : ...
    async def async_is_shared(self)                                         -> bool      : ...
    def             link     (self)                                         -> Executable: ...
    async def async_link     (self)                                         -> Executable: ...
    def             is_linked(self)                                         -> bool      : ...
    async def async_is_linked(self)                                         -> bool      : ...
    dynamic_file   : path
    executable_file: path
    from_code      : Module | Source
    lib_objects    : list[Object]



@member(Object)
def __init__(self: Object, file: path, from_code: Module | Source) -> None:
    super(Object, self).__init__(file)
    self.dynamic_file    = replace_suffix_file(self.file, system.dynamic_suffix)
    self.executable_file = replace_suffix_file(self.file, system.executable_suffix)
    self.from_code       = from_code
    self.lib_objects     = recursive_collect(node=self.from_code, next=lambda code: code.import_modules, collect=lambda code: Object(code.object_file, code))

@member(Object)
@syncable
@once
async def async_share(self: Object) -> Dynamic:
    if not await self.async_is_shared():
        async with scheduler.schedule():
            print(f'share object {self.file}')
            await compiler.async_share(
                object_file =self.file,
                dynamic_file=self.dynamic_file,
                link_flags  =self.link_flags,
                lib_files   =recursive_collect(self,                 next=lambda object : object.lib_objects,       collect=lambda object : object.file) +
                             recursive_collect(self.context_package, next=lambda package: package.require_packages, collect=lambda package: [file for file in iterate_dir(package.install_lib_dir)], flatten=True)
            )
        self.context_package.unit_status_logger.set_object_shared(object=self, shared=True)
    return Dynamic(self.dynamic_file)

@member(Object)
@syncable
@once
async def async_is_shared(self: Object) -> bool:
    return self.context_package.unit_status_logger.get_object_shared(object=self)

@member(Object)
@syncable
@once
async def async_link(self: Object) -> Executable:
    if not await self.async_is_linked():
        async with scheduler.schedule():
            print(f'link object {self.file}')
            await compiler.async_link(
                object_file    =self.file,
                executable_file=self.executable_file,
                link_flags     =self.link_flags,
                lib_files      =recursive_collect(self,                 next=lambda object : object.lib_objects,       collect=lambda object : object.file) +
                                recursive_collect(self.context_package, next=lambda package: package.require_packages, collect=lambda package: [file for file in iterate_dir(package.install_lib_dir)], flatten=True)
            )
        self.context_package.unit_status_logger.set_object_linked(object=self, linked=True)
    return Executable(self.executable_file)

@member(Object)
@syncable
@once
async def async_is_linked(self: Object) -> bool:
    return self.context_package.unit_status_logger.get_object_linked(object=self)