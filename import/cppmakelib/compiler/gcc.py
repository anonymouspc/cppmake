from cppmakelib.basic.config       import config
from cppmakelib.error.config       import ConfigError
from cppmakelib.error.subprocess   import SubprocessError
from cppmakelib.executor.run       import async_run
from cppmakelib.utility.decorator  import member, syncable, unique_on
from cppmakelib.utility.filesystem import get_file_name, is_file, iterate_dir, join_path, new_dir, normal_path, parent_dir, path, resolvable_path, remove_file_suffix, replace_file_suffix, resolve_file
from cppmakelib.utility.version    import Version
import re

class Gcc:
    def           __new__     (cls : type[Gcc], file: resolvable_path = 'g++')                                                                                                                                                                  -> Gcc : ...
    def           __init__    (self: Gcc,       file: resolvable_path = 'g++')                                                                                                                                                                  -> None: ...
    async def    __ainit__    (self: Gcc,       file: resolvable_path = 'g++')                                                                                                                                                                  -> None: ...
    def             preprocess(self: Gcc,       code_file  : path, preprocessed_file: path,                    compile_flags: list[str] = [], define_macros: dict[str, str] = {}, include_dirs: list[path] = [])                                -> None: ...
    async def async_preprocess(self: Gcc,       code_file  : path, preprocessed_file: path,                    compile_flags: list[str] = [], define_macros: dict[str, str] = {}, include_dirs: list[path] = [])                                -> None: ...
    def             preparse  (self: Gcc,       header_file: path, preparsed_file   : path,                    compile_flags: list[str] = [], define_macros: dict[str, str] = {}, include_dirs: list[path] = [])                                -> None: ...
    async def async_preparse  (self: Gcc,       header_file: path, preparsed_file   : path,                    compile_flags: list[str] = [], define_macros: dict[str, str] = {}, include_dirs: list[path] = [])                                -> None: ...
    def             precompile(self: Gcc,       module_file: path, precompiled_file : path, object_file: path, compile_flags: list[str] = [], define_macros: dict[str, str] = {}, import_dirs : list[path] = [], include_dirs: list[path] = []) -> None: ...
    async def async_precompile(self: Gcc,       module_file: path, precompiled_file : path, object_file: path, compile_flags: list[str] = [], define_macros: dict[str, str] = {}, import_dirs : list[path] = [], include_dirs: list[path] = []) -> None: ...
    def             compile   (self: Gcc,       source_file: path, object_file      : path,                    compile_flags: list[str] = [], define_macros: dict[str, str] = {}, import_dirs : list[path] = [], include_dirs: list[path] = []) -> None: ...
    async def async_compile   (self: Gcc,       source_file: path, object_file      : path,                    compile_flags: list[str] = [], define_macros: dict[str, str] = {}, import_dirs : list[path] = [], include_dirs: list[path] = []) -> None: ...
    def             share     (self: Gcc,       object_file: path, dynamic_file     : path,                    link_flags   : list[str] = [],                                     lib_files   : list[path] = [])                                -> None: ...
    async def async_share     (self: Gcc,       object_file: path, dynamic_file     : path,                    link_flags   : list[str] = [],                                     lib_files   : list[path] = [])                                -> None: ...
    def             link      (self: Gcc,       object_file: path, executable_file  : path,                    link_flags   : list[str] = [],                                     lib_files   : list[path] = [])                                -> None: ...
    async def async_link      (self: Gcc,       object_file: path, executable_file  : path,                    link_flags   : list[str] = [],                                     lib_files   : list[path] = [])                                -> None: ...
    preprocessed_suffix: str = 'ipp'
    preparsed_suffix   : str = 'gch'
    precompiled_suffix : str = 'gcm'  
    diagnostic_suffix  : str = 'sarif'
    file               : resolvable_path
    version            : Version
    compile_flags      : list[str]
    link_flags         : list[str]
    define_macros      : dict[str, str]
    stdlib_name        : str = 'libstdc++'
    stdlib_module_file : path
    stdlib_static_file : path
    stdlib_dynamic_file: path

    async def _async_get_version           (self: Gcc)                                                                                 -> Version: ...
    async def _async_get_stdlib_module_file(self: Gcc)                                                                                 -> path   : ...
    def       _write_mapper                (self: Gcc, target_file: path, import_files: list[path] = [], import_dirs: list[path] = []) -> path   : ...



@member(Gcc)
@syncable
@unique_on(resolve_file)
async def __ainit__(self: Gcc, file: resolvable_path = 'g++') -> None:
    self.file    = file
    self.version = await self._async_get_version()
    self.compile_flags = [
        f'-std={config.std}', '-fmodules', 
        *(['-O0', '-g'] if config.type == 'debug'   else
          ['-O3']       if config.type == 'release' else
          ['-Os']       if config.type == 'size'    else 
          []) 
    ]
    self.link_flags = [
        *(['-s'] if config.type == 'release' or config.type == 'size' else []),
        '-lstdc++exp'
    ]
    self.define_macros = {
        **({'DEBUG'  : 'true'} if config.type == 'debug'   else
           {'DNDEBUG': 'true'} if config.type == 'release' else
           {})
    }
    self.stdlib_module_file = await self._async_get_stdlib_module_file()

@member(Gcc)
@syncable
async def async_preprocess(
    self             : Gcc, 
    code_file        : path, 
    preprocessed_file: path, 
    compile_flags    : list[str]      = [], 
    define_macros    : dict[str, str] = {}, 
    include_dirs     : list[path]     = []
) -> None:
    new_dir(parent_dir(preprocessed_file), exist_ok=True)
    await async_run(
        file=self.file,
        args=[
            *(self.compile_flags + compile_flags),
            *[f'-D{key}={value}' for key, value  in (self.define_macros | define_macros).items()],
            *[f'-I{include_dir}' for include_dir in include_dirs],
            '-E', code_file,
            '-o', preprocessed_file
        ],
        print_stdout=False,
    )

@member(Gcc)
@syncable
async def async_preparse(
    self           : Gcc,
    header_file    : path,
    preparsed_file : path,
    compile_flags  : list[str]      = [],
    define_macros  : dict[str, str] = {},
    include_dirs   : list[path]     = []
) -> None:
    new_dir(parent_dir(preparsed_file), exist_ok=True)
    await async_run(
        file=self.file,
        args=[
            *(self.compile_flags + compile_flags),
            *[f'-D{key}={value}' for key, value  in (self.define_macros | define_macros).items()],
            *[f'-I{include_dir}' for include_dir in include_dirs],
            f'-fdiagnostics-add-output=sarif:file={replace_file_suffix(preparsed_file, 'sarif')}',
            '-c', '-x', 'c++-header', header_file,
            '-o', preparsed_file
        ],
        log_command=header_file
    )
    
@member(Gcc)
@syncable
async def async_precompile(
    self            : Gcc, 
    module_file     : path, 
    precompiled_file: path, 
    object_file     : path, 
    compile_flags   : list[str]      = [], 
    define_macros   : dict[str, str] = {}, 
    import_dirs     : list[path]     = [], 
    include_dirs    : list[path]     = []
) -> None:
    new_dir(parent_dir(precompiled_file), exist_ok=True)
    new_dir(parent_dir(object_file))
    await async_run(
        file=self.file,
        args=[
            *(self.compile_flags + compile_flags),
            *[f'-D{key}={value}' for key, value  in (self.define_macros | define_macros).items()],
            f'-fmodule-mapper={self._write_mapper(target_file=precompiled_file, import_files=[precompiled_file],  import_dirs=import_dirs)}',
            *[f'-I{include_dir}' for include_dir in include_dirs],
            f'-fdiagnostics-add-output=sarif:file={replace_file_suffix(precompiled_file, 'sarif')}'
            '-c', '-x', 'c++', module_file,
            '-o', object_file
        ],
        log_command=module_file
    )

@member(Gcc)
@syncable
async def async_compile(
    self           : Gcc, 
    source_file    : path,
    object_file    : path,
    compile_flags  : list[str]      = [],
    define_macros  : dict[str, str] = {}, 
    import_dirs    : list[path]     = [], 
    include_dirs   : list[path]     = []
) -> None:
    new_dir(parent_dir(object_file), exist_ok=True)
    await async_run(
        file=self.file,
        args=[
            *(self.compile_flags + compile_flags),
            *[f'-D{key}={value}' for key, value  in (self.define_macros | define_macros).items()],
            f'-fmodule-mapper={self._write_mapper(target_file=object_file, import_dirs=import_dirs)}',
            *[f'-I{include_dir}' for include_dir in include_dirs],
            f'-fdiagnostics-add-output=sarif:file={replace_file_suffix(object_file, 'sarif')}'
            '-c', '-x', 'c++', source_file,
            '-o', object_file
        ],
        log_command=source_file
    )

@member(Gcc)
@syncable
async def async_link(
    self           : Gcc, 
    object_file    : path, 
    executable_file: path, 
    link_flags     : list[str]  = [], 
    lib_files      : list[path] = []
) -> None:
    new_dir(parent_dir(executable_file), exist_ok=True)
    await async_run(
        file=self.file,
        args=[
            *(self.link_flags + link_flags),
            *([object_file] + lib_files),
            '-o', executable_file
        ]
    )

@member(Gcc)
async def _async_get_version(self: Gcc) -> Version:
    try:
        stdout = await async_run(
            file=self.file,
            args=['--version'],
            print_stdout=config.verbose,
            return_stdout=True
        )
    except SubprocessError as error:
        raise ConfigError(f'gcc check failed (with file = {self.file})') from error
    try:
        version = Version.parse(pattern=r'^g\+\+\w* \(.*\) (\d+)\.(\d+)\.(\d+)', string=stdout.splitlines()[0])
    except Version.ParseError as error:
        raise ConfigError(f'gcc check failed (with file = {self.file})') from error
    if version < 15:
        raise ConfigError(f'gcc version is too old (with file = {self.file}, version = {version}, requires = 15+)')
    return version

@member(Gcc)
async def _async_get_stdlib_module_file(self: Gcc) -> path:
    stderr = await async_run(
        file=self.file,
        args=[
            *self.compile_flags,
            '-E', '-x', 'c++', '-',
            '-v' 
        ],
        env=current_env.copy().update({'LANG': 'C'}),
        print_stderr=config.verbose,
        return_stderr=True
    )
    search_dirs = re.search(
        pattern=r'^#include <...> search starts here:$\n((?:^.*$\n)*)^End of search list.$', 
        string =stderr, 
        flags  =re.MULTILINE
    )
    if search_dirs is None:
        raise ConfigError('libstdc++ module_file is not found')
    search_dirs  = [path(search_dir.strip())                for search_dir in search_dirs.group(1).splitlines()]
    search_files = [join_path(search_dir, 'bits', 'std.cc') for search_dir in search_dirs]
    for search_file in search_files:
        if is_file(search_file):
            return normal_path(search_file)
    else:
        raise ConfigError(f'libstdc++ module_file is not found (with search_files = {search_files})')

@member(Gcc)
def _write_mapper(self: Gcc, target_file: path, import_files: list[path] = [], import_dirs: list[path] = []) -> path:
    mapper_file = replace_file_suffix(target_file, 'mapper')
    writer = open(mapper_file, 'w')
    for file in import_files + [import_file for import_dir in import_dirs for import_file in iterate_dir(import_dir) if import_file.endswith(Gcc.precompiled_suffix)]:
        name = get_file_name(remove_file_suffix(file)).replace('-', ':')
        writer.write(f'{name} {file}\n')
    writer.close()
    return mapper_file
    