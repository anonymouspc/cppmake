from cppmakelib.compiler.all       import compiler
from cppmakelib.executor.operation import then, when_all
from cppmakelib.executor.scheduler import scheduler
from cppmakelib.package.all        import context
from cppmakelib.system.all         import system
from cppmakelib.unit.header        import Header
from cppmakelib.unit.module        import Module
from cppmakelib.unit.object        import Object
from cppmakelib.utility.algorithm  import recursive_collect
from cppmakelib.utility.decorator  import member, once, pre, syncable, unique_in
from cppmakelib.utility.filesystem import get_file_modify_time, join_path, normal_path, path, relative_path, replace_file_suffix
from cppmakelib.utility.time       import time

class Source:
    def           __new__      (cls : type[Source], file: path) -> Source: ...
    def           __init__     (self: Source,       file: path) -> None  : ...
    async def    __ainit__     (self: Source,       file: path) -> None  : ...
    def             compile    (self: Source)                   -> Object: ...
    async def async_compile    (self: Source)                   -> Object: ...
    def             is_compiled(self: Source)                   -> bool  : ...
    async def async_is_compiled(self: Source)                   -> bool  : ...
    file             : path
    build_object_file: path
    modify_time      : time
    compile_flags    : list[str]
    define_macros    : dict[str, str]
    import_modules   : list[Module]
    include_headers  : list[Header]



@member(Source)
@syncable
@unique_in(context.package)
@pre(1, normal_path)
async def __ainit__(self: Source, file: path) -> None:
    self.file            = file
    self.modify_time     = get_file_modify_time(self.file)
    self.object_file     = join_path(context.package.build_dir, replace_file_suffix(relative_path(from_path=context.package.dir, to_path=file), system.object_suffix))
    self.compile_flags   = context.package.compile_flags
    self.define_macros   = context.package.define_macros
    self.import_modules  = await when_all([then(Module.__new__(Module, file), lambda module: module.__ainit__(file)) for file in await context.package.unit_status_cacher.async_get_imports (code=self)])
    self.include_headers = await when_all([then(Header.__new__(Header, file), lambda header: header.__ainit__(file)) for file in await context.package.unit_status_cacher.async_get_includes(code=self)])

@member(Source)
@syncable
@once
async def async_compile(self: Source) -> Object:
    if not await self.async_is_compiled():
        await when_all([module.async_precompile() for module in self.import_modules ])
        await when_all([header.async_preparse()   for header in self.include_headers])
        async with scheduler.schedule():
            print(f'compile source {self.file}')
            await compiler.async_compile(
                source_file    =self.file,
                object_file    =self.object_file,
                compile_flags  =self.compile_flags,
                define_macros  =self.define_macros,
                import_dirs    =[context.package.build_import_dir]  + recursive_collect(context.package, next=lambda package: package.require_packages, collect=lambda package: package.install_import_dir),                    
                include_dirs   =[context.package.build_include_dir] + recursive_collect(context.package, next=lambda package: package.require_packages, collect=lambda package: package.install_include_dir),
            )
        context.package.unit_status_cacher.set_compiled(source=self, compiled=True)
    return Object(self.object_file, from_code=self)

@member(Source)
@syncable
@once
async def async_is_compiled(self: Source) -> bool:
    return all(await when_all([module.async_is_precompiled() for module in self.import_modules ])) and \
           all(await when_all([header.async_is_preparsed()   for header in self.include_headers])) and \
           context.package.unit_status_cacher.get_compiled(source=self)
