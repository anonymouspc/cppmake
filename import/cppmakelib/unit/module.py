from cppmakelib.basic.context      import context
from cppmakelib.compiler.all       import compiler
from cppmakelib.executor.operation import then, when_all
from cppmakelib.executor.scheduler import scheduler
from cppmakelib.system.all         import system
from cppmakelib.unit.code          import Code
from cppmakelib.unit.precompiled   import Precompiled
from cppmakelib.utility.algorithm  import recursive_collect
from cppmakelib.utility.decorator  import member, pre, once, syncable, unique_in
from cppmakelib.utility.filesystem import add_file_suffix, join_path, normal_path, path

class Module(Code):
    def           __new__         (cls : type[Module], file: path) -> Module     : ...
    def           __init__        (self: Module,       file: path) -> None       : ...
    async def    __ainit__        (self: Module,       file: path) -> None       : ...
    def             precompile    (self: Module)                   -> Precompiled: ...
    async def async_precompile    (self: Module)                   -> Precompiled: ...
    def             is_precompiled(self: Module)                   -> bool       : ...
    async def async_is_precompiled(self: Module)                   -> bool       : ...
    name            : str
    precompiled_file: path
    object_file     : path
    import_modules  : list[Module]



@member(Module)
@syncable
@unique_in(context.package)
@pre(1, normal_path)
async def __ainit__(self: Module, file: path) -> None:
    await super(Module, self).__ainit__(file)
    self.name             = await self.context_package.unit_status_cacher.async_get_module_name(module=self)
    self.precompiled_file = join_path(self.context_package.build_import_dir, add_file_suffix(self.name.replace(':', '-'), compiler.precompiled_suffix))
    self.object_file      = join_path(self.context_package.build_import_dir, add_file_suffix(self.name.replace(':', '-'), system.object_suffix))
    self.import_modules   = await when_all([then(Module.__new__(Module, ), lambda module: module.__ainit__(name)) for name in await self.context_package.unit_status_cacher.async_get_module_imports(module=self)])

@member(Module)
@syncable
@once
async def async_precompile(self: Module) -> Precompiled:
    if not await self.async_is_precompiled():
        await when_all([module.async_precompile() for module in self.import_modules])
        await self.async_preprocess()
        async with scheduler.schedule():
            print(f'precompile module {self.file}')
            await compiler.async_precompile(
                module_file     =self.file,
                precompiled_file=self.precompiled_file,
                object_file     =self.object_file,
                compile_flags   =self.compile_flags,
                define_macros   =self.define_macros,
                import_dirs     =[self.context_package.build_import_dir]  + recursive_collect(self.context_package, next=lambda package: package.require_packages, collect=lambda package: package.install_import_dir),
                include_dirs    =[self.context_package.build_include_dir] + recursive_collect(self.context_package, next=lambda package: package.require_packages, collect=lambda package: package.install_include_dir),
            )
        self.context_package.unit_status_cacher.set_module_precompiled(module=self, precompiled=True)
    return Precompiled(self.precompiled_file)

@member(Module)
@syncable
@once
async def async_is_precompiled(self: Module) -> bool:
    return all(await when_all([module.async_is_precompiled() for module in self.import_modules ])) and \
           await self.async_is_preprocessed()                                                      and \
           self.context_package.unit_status_cacher.get_module_precompiled(module=self)

