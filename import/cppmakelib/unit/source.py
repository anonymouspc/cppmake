from cppmakelib.basic.context      import context
from cppmakelib.compiler.all       import compiler
from cppmakelib.executor.operation import then, when_all
from cppmakelib.executor.scheduler import scheduler
from cppmakelib.system.all         import system
from cppmakelib.unit.code          import Code
from cppmakelib.unit.module        import Module
from cppmakelib.utility.algorithm  import recursive_collect
from cppmakelib.utility.decorator  import member, once, pre, syncable, unique_in
from cppmakelib.utility.filesystem import join_path, normal_path, path, relative_path, replace_file_suffix

class Source(Code):
    def           __new__      (cls : type[Source], file: path) -> Source: ...
    def           __init__     (self: Source,       file: path) -> None  : ...
    async def    __ainit__     (self: Source,       file: path) -> None  : ...
    def             compile    (self: Source)                   -> Object: ...
    async def async_compile    (self: Source)                   -> Object: ...
    def             is_compiled(self: Source)                   -> bool  : ...
    async def async_is_compiled(self: Source)                   -> bool  : ...
    object_file    : path
    import_modules : list[Module]



from cppmakelib.unit.object        import Object

@member(Source)
@syncable
@unique_in(context.package)
@pre(1, normal_path)
async def __ainit__(self: Source, file: path) -> None:
    await super(Source, self).__ainit__(file)
    self.object_file    = join_path(self.context_package.build_dir, replace_file_suffix(relative_path(from_path=self.context_package.dir, to_path=file), system.object_suffix))
    self.import_modules = await when_all([then(Module.__new__(Module, file), lambda module: module.__ainit__(file)) for file in await self.context_package.unit_status_cacher.async_get_source_imports(source=self)])

@member(Source)
@syncable
@once
async def async_compile(self: Source) -> Object:
    if not await self.async_is_compiled():
        await when_all([module.async_precompile() for module in self.import_modules ])
        await self.async_preprocess()
        async with scheduler.schedule():
            print(f'compile source {self.file}')
            await compiler.async_compile(
                source_file    =self.file,
                object_file    =self.object_file,
                compile_flags  =self.compile_flags,
                define_macros  =self.define_macros,
                import_dirs    =[self.context_package.build_import_dir]  + recursive_collect(self.context_package, next=lambda package: package.require_packages, collect=lambda package: package.install_import_dir),                    
                include_dirs   =[self.context_package.build_include_dir] + recursive_collect(self.context_package, next=lambda package: package.require_packages, collect=lambda package: package.install_include_dir),
            )
        self.context_package.unit_status_cacher.set_source_compiled(source=self, compiled=True)
    return Object(self.object_file, from_=self)

@member(Source)
@syncable
@once
async def async_is_compiled(self: Source) -> bool:
    return all(await when_all([module.async_is_precompiled() for module in self.import_modules ])) and \
           await self.async_is_preprocessed()                                                      and \
           self.context_package.unit_status_cacher.get_source_compiled(source=self)
