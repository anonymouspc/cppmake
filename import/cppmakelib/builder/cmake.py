from cppmakelib.basic.config       import config
from cppmakelib.compiler.all       import compiler
from cppmakelib.error.config       import ConfigError
from cppmakelib.error.subprocess   import SubprocessError
from cppmakelib.executor.run       import async_run
from cppmakelib.utility.decorator  import member, syncable, unique_on
from cppmakelib.utility.filesystem import delete_dir, new_dir, parent_dir, path, resolvable_path, resolve_file
from cppmakelib.utility.version    import Version

class Cmake: 
    def           __new__    (cls : type[Cmake], file: resolvable_path = 'cmake')                                                         -> Cmake: ...
    def           __init__   (self: Cmake,       file: resolvable_path = 'cmake')                                                         -> None : ...
    async def    __ainit__   (self: Cmake,       file: resolvable_path = 'cmake')                                                         -> None : ...
    def             configure(self: Cmake,       cmakelists_file: path, build_dir: path, build_flags: list[str], prefix_dirs: list[path]) -> None : ...
    async def async_configure(self: Cmake,       cmakelists_file: path, build_dir: path, build_flags: list[str], prefix_dirs: list[path]) -> None : ...
    def             build    (self: Cmake,       build_dir: path)                                                                         -> None : ...
    async def async_build    (self: Cmake,       build_dir: path)                                                                         -> None : ...
    def             install  (self: Cmake,       build_dir: path, install_dir: path)                                                      -> None : ...
    async def async_install  (self: Cmake,       build_dir: path, install_dir: path)                                                      -> None : ...
    file       : resolvable_path
    version    : Version
    build_flags: list[str]

    async def _async_get_version(self: Cmake) -> Version: ...

cmake: Cmake



@member(Cmake)
@syncable
@unique_on(resolve_file)
async def __ainit__(self: Cmake, file: resolvable_path = 'cmake') -> None:
    self.file        = file
    self.version     = await self._async_get_version()
    self.build_flags = [
        f'-DCMAKE_BUILD_TYPE={config.type.capitalize()}',
        f'-DCMAKE_CXX_COMPILER={compiler.file}',
        f'-DCMAKE_CXX_FLAGS={compiler.compile_flags}'
    ]

@member(Cmake)
@syncable
async def async_configure(
    self: Cmake, 
    cmakelists_file: path,
    build_dir      : path,
    build_flags    : list[str], 
    prefix_dirs    : list[path]
) -> None:
    try:
        new_dir(build_dir) # Must configure in a new empty dir.
        await async_run(
            file=self.file,
            args=[
                *(self.build_flags + build_flags),
                f'-DCMAKE_PREFIX_PATH={';'.join(prefix_dirs)}',
                '-S', parent_dir(cmakelists_file),
                '-B', build_dir,
            ]
        )
    except:
        delete_dir(build_dir, not_exist_ok=True)
        raise

@member(Cmake)
@syncable
async def async_build(
    self     : Cmake, 
    build_dir: path
) -> None:
    await async_run(
        file=self.file,
        args=[
            '--build', build_dir,
            '-j',      str(config.jobs)
        ]
    )

@member(Cmake)
@syncable
async def async_install(
    self       : Cmake,
    build_dir  : path,
    install_dir: path
) -> None:
    try:
        new_dir(install_dir, exist_ok=True)
        await async_run(
            file=self.file,
            args=[
                '--install', build_dir,
                '--prefix',  install_dir,
                '-j',        str(config.jobs)
            ]
        )
    except:
        delete_dir(install_dir, not_exist_ok=True)
        raise

@member(Cmake)
async def _async_get_version(self: Cmake) -> Version:
    try:
        stdout = await async_run(
            file=self.file,
            args=['--version'],
            return_stdout=True
        )
    except SubprocessError as error:
        raise ConfigError(f'cmake check failed (with file = {self.file})') from error
    try:
        version = Version.parse(pattern=r'^cmake version (\d+)\.(\d+)\.(\d+)', string=stdout.splitlines()[0])
    except Version.ParseError as error:
        raise ConfigError(f'cmake check failed (with file = {self.file})') from error
    if version < 4:
        raise ConfigError(f'cmake version is too old (with file = {self.file}, version = {version}, requires = 4+)')
    return version

cmake = Cmake()