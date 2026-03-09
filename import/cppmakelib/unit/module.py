from cppmakelib.package.all        import context
from cppmakelib.compiler.all       import compiler
from cppmakelib.executor.operation import then, when_all
from cppmakelib.executor.scheduler import scheduler
from cppmakelib.system.all         import system
from cppmakelib.unit.header        import Header
from cppmakelib.unit.precompiled   import Precompiled
from cppmakelib.utility.algorithm  import recursive_collect
from cppmakelib.utility.decorator  import member, pre, once, syncable, unique_in
from cppmakelib.utility.filesystem import add_file_suffix, get_file_modify_time, is_file, join_path, normal_path, path
from cppmakelib.utility.time       import time

class Module:
    def           __new__         (cls : type[Module], file: path) -> Module     : ...
    def           __init__        (self: Module,       file: path) -> None       : ...
    async def    __ainit__        (self: Module,       file: path) -> None       : ...
    def             precompile    (self: Module)                   -> Precompiled: ...
    async def async_precompile    (self: Module)                   -> Precompiled: ...
    def             is_precompiled(self: Module)                   -> bool       : ...
    async def async_is_precompiled(self: Module)                   -> bool       : ...
    file            : path
    precompiled_file: path
    object_file     : path
    name            : str
    modify_time     : time
    compile_flags   : list[str]
    define_macros   : dict[str, str]
    import_modules  : list[Module]
    include_headers : list[Header]



@member(Module)
@syncable
@unique_in(context.package)
@pre(1, normal_path)
async def __ainit__(self: Module, file: path) -> None:
    self.file             = file
    self.modify_time      = get_file_modify_time(self.file)
    self.name             = await context.package.unit_status_cacher.async_get_export(code=self)
    self.precompiled_file = join_path(context.package.build_import_dir, add_file_suffix(self.name.replace(':', '-'), compiler.precompiled_suffix))
    self.object_file      = join_path(context.package.build_import_dir, add_file_suffix(self.name.replace(':', '-'), system.object_suffix))
    self.import_modules   = await when_all([then(Module.__new__(Module, file), lambda module: module.__ainit__(file)) for file in await context.package.unit_status_cacher.async_get_imports (code=self) if is_file(file)])
    self.include_headers  = await when_all([then(Header.__new__(Header, file), lambda header: header.__ainit__(file)) for file in await context.package.unit_status_cacher.async_get_includes(code=self) if is_file(file)])

@member(Module)
@syncable
@once
async def async_precompile(self: Module) -> Precompiled:
    if not await self.async_is_precompiled():
        await when_all([module.async_precompile() for module in self.import_modules ])
        await when_all([header.async_preparse()   for header in self.include_headers])
        async with scheduler.schedule():
            print(f'precompile module {self.file}')
            await compiler.async_precompile(
                module_file     =self.file,
                precompiled_file=self.precompiled_file,
                object_file     =self.object_file,
                compile_flags   =self.compile_flags,
                define_macros   =self.define_macros,
                import_dirs     =[context.package.build_import_dir]  + recursive_collect(context.package, next=lambda package: package.require_packages, collect=lambda package: package.install_import_dir),
                include_dirs    =[context.package.build_include_dir] + recursive_collect(context.package, next=lambda package: package.require_packages, collect=lambda package: package.install_include_dir),
            )
        context.package.unit_status_cacher.set_precompiled(module=self, precompiled=True)
    return Precompiled(self.precompiled_file)

@member(Module)
@syncable
@once
async def async_is_precompiled(self: Module) -> bool:
    return all(await when_all([module.async_is_precompiled() for module in self.import_modules ])) and \
           all(await when_all([header.async_is_preparsed()   for header in self.include_headers])) and \
           context.package.unit_status_cacher.get_precompiled(module=self)

