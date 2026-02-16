from cppmakelib.basic.config       import config
from cppmakelib.compiler.gcc       import Gcc
from cppmakelib.error.config       import ConfigError
from cppmakelib.error.subprocess   import SubprocessError
from cppmakelib.executor.run       import async_run
from cppmakelib.utility.decorator  import member, syncable, unique_on
from cppmakelib.utility.filesystem import is_file, join_path, normal_path, new_dir, parent_dir, path, resolve_file, resolvable_path
from cppmakelib.utility.version    import Version

class Clang(Gcc):
    def           __new__     (cls : type[Clang], file: resolvable_path = 'clang++')                                                                                                                                                             -> Clang: ...
    def           __init__    (self: Clang,       file: resolvable_path = 'clang++')                                                                                                                                                             -> None : ...
    async def    __ainit__    (self: Clang,       file: resolvable_path = 'clang++')                                                                                                                                                             -> None : ...
    def             precompile(self: Clang,       module_file: path, precompiled_file: path, object_file: path, compile_flags: list[str] = [], define_macros: dict[str, str] = {}, import_dirs : list[path] = [], include_dirs: list[path] = []) -> None : ...
    async def async_precompile(self: Clang,       module_file: path, precompiled_file: path, object_file: path, compile_flags: list[str] = [], define_macros: dict[str, str] = {}, import_dirs : list[path] = [], include_dirs: list[path] = []) -> None : ...
    def             preparse  (self: Clang,       header_file: path, preparsed_file  : path,                    compile_flags: list[str] = [], define_macros: dict[str, str] = {}, include_dirs: list[path] = [])                                -> None : ...
    async def async_preparse  (self: Clang,       header_file: path, preparsed_file  : path,                    compile_flags: list[str] = [], define_macros: dict[str, str] = {}, include_dirs: list[path] = [])                                -> None : ...
    def             compile   (self: Clang,       source_file: path, object_file     : path,                    compile_flags: list[str] = [], define_macros: dict[str, str] = {}, import_dirs : list[path] = [], include_dirs: list[path] = []) -> None : ...
    async def async_compile   (self: Clang,       source_file: path, object_file     : path,                    compile_flags: list[str] = [], define_macros: dict[str, str] = {}, import_dirs : list[path] = [], include_dirs: list[path] = []) -> None : ...
    preparsed_suffix   : str = 'pch'
    precompiled_suffix : str = 'pcm'
    file               : resolvable_path
    version            : Version
    compile_flags      : list[str]
    link_flags         : list[str]
    define_macros      : dict[str, str]
    stdlib_name        : str
    stdlib_module_file : path
    stdlib_static_file : path
    stdlib_dynamic_file: path

    async def _async_get_version           (self: Clang) -> Version: ...
    async def _async_get_stdlib_name       (self: Clang) -> str    : ...
    async def _async_get_stdlib_module_file(self: Clang) -> path   : ...



@member(Clang)
@syncable
@unique_on(resolve_file)
async def __ainit__(self: Clang, file: resolvable_path = 'clang++') -> None:
    self.file        = file
    self.version     = await self._async_get_version()
    self.compile_flags = [
       f'-std={config.std}',
        *(['-O0', '-g'] if config.type == 'debug'   else
          ['-O3']       if config.type == 'release' else
          ['-Os']       if config.type == 'size'    else 
          [])
    ]
    self.link_flags = [
        *(['-s']          if config.type == 'release' or config.type == 'size' else []),
        *(['-lstdc++exp'] if self.stdlib_name == 'libstdc++'                   else [])
    ]
    self.define_macros = {
        **({'DEBUG' : 'true'} if config.type == 'debug'   else 
           {'NDEBUG': 'true'} if config.type == 'release' else 
           {})
    }
    self.stdlib_name        = await self._async_get_stdlib_name()
    self.stdlib_module_file = await self._async_get_stdlib_module_file()

@member(Clang)
@syncable
async def async_preparse(
    self           : Clang,
    header_file    : path,
    preparsed_file : path,
    compile_flags  : list[str]      = [],
    define_macros  : dict[str, str] = {},
    include_dirs   : list[path]     = [],
) -> None:
    new_dir(parent_dir(preparsed_file), exist_ok=True)
    await async_run(
        file=self.file,
        args=[
            *(self.compile_flags + compile_flags),
            *[f'-D{key}={value}' for key, value  in (self.define_macros | define_macros).items()],
            *[f'-I{include_dir}' for include_dir in include_dirs],
            '-c', '-x', 'c++-header', header_file,
            '-o', preparsed_file
        ],
        log_command=header_file
    )


@member(Clang)
@syncable
async def async_precompile(
    self            : Clang, 
    module_file     : path, 
    precompiled_file: path, 
    object_file     : path, 
    compile_flags   : list[str]      = [], 
    define_macros   : dict[str, str] = {}, 
    import_dirs     : list[path]     = [], 
    include_dirs    : list[path]     = [], 
) -> None:
    new_dir(parent_dir(precompiled_file), exist_ok=True)
    new_dir(parent_dir(object_file),      exist_ok=True)
    await async_run(
        file=self.file,
        args=[
            *(self.compile_flags + compile_flags),
            *[f'-D{key}={value}' for key, value  in (self.define_macros | define_macros).items()],
            *[f'-fprebuilt-module-path={import_dir}' for import_dir in import_dirs],
            *[f'-I{include_dir}' for include_dir in include_dirs],
            '--precompile', '-x', 'c++-module', module_file,
            '-o', precompiled_file
        ],
        log_command=module_file
    )
    await async_run(
        file=self.file,
        args=[
            *[f'-fprebuilt-module-path={import_dir}' for import_dir in import_dirs],
            '-c', precompiled_file,
            '-o', object_file
        ]
    )

@member(Clang)
@syncable
async def async_compile(
    self: Clang, 
    source_file    : path, 
    object_file    : path, 
    compile_flags  : list[str]      = [], 
    define_macros  : dict[str, str] = {}, 
    import_dirs    : list[path]     = [], 
    include_dirs   : list[path]     = [], 
) -> None:
    new_dir(parent_dir(object_file), exist_ok=True)
    await async_run(
        file=self.file,
        args=[
            *(self.compile_flags + compile_flags),
            *[f'-D{key}={value}' for key, value  in (self.define_macros | define_macros).items()],
            *[f'-fprebuilt-module-path={import_dir}' for import_dir in import_dirs],
            *[f'-I{include_dir}' for include_dir in include_dirs],
            '-c', '-x', 'c++', source_file,
            '-o', object_file
        ],
        log_command=source_file
    )

@member(Clang)
async def _async_get_version(self: Clang) -> Version:
    try:
        stdout = await async_run(
            file=self.file,
            args=['--version'],
            return_stdout=True
        )
    except SubprocessError as error:
        raise ConfigError(f'clang check failed (with file = {self.file})') from error
    try:
        version = Version.parse(pattern=r'clang version (\d+)\.(\d+)\.(\d+)', string=stdout.splitlines()[0])
    except Version.ParseError as error:
        raise ConfigError(f'clang check failed (with file = {self.file})') from error
    if version < 21:
        raise ConfigError(f'clang version is too old (with file = {self.file}, version = {version}, requires = 21+)')
    return version

@member(Clang)
async def _async_get_stdlib_name(self: Clang) -> str:
    stderr = await async_run(
        file=self.file,
        args=[
            *self.compile_flags,
            '-v',
        ],
        print_stderr=config.verbose,
        return_stderr=True
    )
    if 'selected gcc installation' in stderr.lower():
        return 'libstdc++'
    else:
        return 'libc++'    

@member(Clang)
async def _async_get_stdlib_module_file(self: Clang) -> path:
    if self.stdlib_name == 'libc++':
        resource_dir = await async_run(
            file=self.file,
            args=['--print-resource-dir'],
            return_stdout=True,
        )
        resource_dir = path(resource_dir.strip())
        search_file = join_path(parent_dir(parent_dir(parent_dir(resource_dir))), 'share', 'libc++', 'v1', 'std.cppm')
        if is_file(search_file): 
            return normal_path(search_file)
        else:
            raise ConfigError(f'libc++ module_file is not found (with search_file = {search_file})')
    elif self.stdlib_name == 'libstdc++':
        return await Gcc._async_get_stdlib_module_file(self)
    else:
        assert False
