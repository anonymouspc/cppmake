from cppmakelib.compiler.all       import compiler
from cppmakelib.executor.operation import then, when_all
from cppmakelib.executor.scheduler import scheduler
from cppmakelib.package.all        import context
from cppmakelib.unit.preparsed     import Preparsed
from cppmakelib.utility.algorithm  import recursive_collect
from cppmakelib.utility.decorator  import member, once, pre, syncable, unique_in
from cppmakelib.utility.filesystem import add_file_suffix, equivalent_path, get_file_modify_time, is_file, join_path, new_hardlink, normal_path, path, relative_path
from cppmakelib.utility.time       import time

class Header:
    def           __new__       (cls : type[Header], file: path) -> Header   : ...
    def           __init__      (self: Header,       file: path) -> None     : ...
    async def    __ainit__      (self: Header,       file: path) -> None     : ...
    def             preparse    (self: Header)                   -> Preparsed: ...
    async def async_preparse    (self: Header)                   -> Preparsed: ...
    def             is_preparsed(self: Header)                   -> bool     : ...
    async def async_is_preparsed(self: Header)                   -> bool     : ...
    def             install     (self: Header)                   -> None     : ...
    async def async_install     (self: Header)                   -> None     : ...
    def             is_installed(self: Header)                   -> bool     : ...
    async def async_is_installed(self: Header)                   -> bool     : ...
    file          : path
    header_file   : path
    preparsed_file: path
    install_file        : path
    modify_time         : time
    header_file         : path
    compile_flags       : list[str]
    define_macros       : dict[str, str]
    include_headers     : list[Header]



@member(Header)
@syncable
@unique_in(context.package)
@pre(1, normal_path)
async def __ainit__(self: Header, file: path) -> None:
    self.file            = file
    self.modify_time     = get_file_modify_time(self.file)
    self.header_file     = join_path(context.package.build_include_dir, relative_path(from_path=context.package.include_dir, to_path=self.file))
    self.preparsed_file  = join_path(context.package.build_include_dir, add_file_suffix(relative_path(from_path=context.package.include_dir, to_path=self.file), compiler.preparsed_suffix))
    self.compile_flags   = context.package.compile_flags
    self.define_macros   = context.package.define_macros
    self.include_headers = await when_all([then(Header.__new__(Header, file), lambda header: header.__ainit__(file)) for file in await context.package.unit_status_cacher.async_get_includes(code=self) if is_file(file)])
    self.install_file    = join_path(context.package.install_include_dir, relative_path(from_path=context.package.include_dir, to_path=self.file))

@member(Header)
@syncable
@once
async def async_preparse(self: Header) -> Preparsed:
    if not await self.async_is_preparsed():
        await when_all([header.async_preparse() for header in self.include_headers])
        async with scheduler.schedule():
            print(f'preparse header {self.file}')
            new_hardlink(from_hardlink=self.header_file, to_path=self.file)
            await compiler.async_preparse(
                header_file      =self.file,
                preparsed_file   =self.preparsed_file,
                compile_flags    =self.compile_flags,
                define_macros    =self.define_macros,
                include_dirs     =[context.package.build_include_dir] + recursive_collect(context.package, next=lambda package: package.require_packages, collect=lambda package: package.install_include_dir),
            )
        context.package.unit_status_cacher.set_preparsed(header=self, preparsed=True)
    return Preparsed(self.preparsed_file, from_header=self)

@member(Header)
@syncable
@once
async def async_is_preparsed(self: Header) -> bool:
    return all(await when_all([header.async_is_preparsed() for header in self.include_headers])) and \
           context.package.unit_status_cacher.get_preparsed(header=self)

@member(Header)
@syncable
@once
async def async_install(self: Header) -> None:
    if not await self.async_is_installed():
        await self.async_preparse()
        await when_all([header.async_install() for header in self.include_headers])
        async with scheduler.schedule():
            print(f'install header {self.file}')
            new_hardlink(from_hardlink=self.install_file, to_path=self.header_file)

@member(Header)
@syncable
@once
async def async_is_installed(self: Header) -> bool:
    return is_file(self.install_file) and equivalent_path(self.install_file, self.file)
