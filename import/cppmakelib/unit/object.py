from cppmakelib.basic.context      import context
from cppmakelib.compiler.all       import compiler
from cppmakelib.executor.scheduler import scheduler
from cppmakelib.system.all         import system
from cppmakelib.unit.binary        import Binary
from cppmakelib.unit.dynamic       import Dynamic
from cppmakelib.unit.executable    import Executable
from cppmakelib.utility.algorithm  import recursive_collect
from cppmakelib.utility.decorator  import member, once, pre, syncable, unique_in
from cppmakelib.utility.filesystem import iterate_dir, normal_path, path, replace_file_suffix
import typing

class Object(Binary):
    def           __new__    (cls : type[Object], file: path, from_: typing.Any) -> Object    : ...
    def           __init__   (self: Object,       file: path, from_: typing.Any) -> None      : ...
    def             share    (self: Object)                                      -> Dynamic   : ...
    async def async_share    (self: Object)                                      -> Dynamic   : ...
    def             is_shared(self: Object)                                      -> bool      : ...
    async def async_is_shared(self: Object)                                      -> bool      : ...
    def             link     (self: Object)                                      -> Executable: ...
    async def async_link     (self: Object)                                      -> Executable: ...
    def             is_linked(self: Object)                                      -> bool      : ...
    async def async_is_linked(self: Object)                                      -> bool      : ...
    from_          : typing.Any 
    dynamic_file   : path
    executable_file: path
    lib_objects    : list[Object]
    


@member(Object)
@unique_in(context.package)
@pre(1, normal_path)
def __init__(self: Object, file: path, from_: typing.Any) -> None:
    super(Object, self).__init__(file)
    self.from_           = from_
    self.dynamic_file    = replace_file_suffix(self.file, system.dynamic_suffix)
    self.executable_file = replace_file_suffix(self.file, system.executable_suffix)
    self.lib_objects     = [Object(module.object_file, from_=module) for module in self.from_.import_modules]

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
        self.context_package.unit_status_cacher.set_object_shared(object=self, shared=True)
    return Dynamic(self.dynamic_file)

@member(Object)
@syncable
@once
async def async_is_shared(self: Object) -> bool:
    return self.context_package.unit_status_cacher.get_object_shared(object=self)

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
        self.context_package.unit_status_cacher.set_object_linked(object=self, linked=True)
    return Executable(self.executable_file)

@member(Object)
@syncable
@once
async def async_is_linked(self: Object) -> bool:
    return self.context_package.unit_status_cacher.get_object_linked(object=self)