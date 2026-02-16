from cppmakelib.basic.config       import config
from cppmakelib.compiler.all       import compiler
from cppmakelib.error.config       import ConfigError
from cppmakelib.error.subprocess   import SubprocessError
from cppmakelib.executor.run       import async_run
from cppmakelib.utility.decorator  import member, syncable, unique_on
from cppmakelib.utility.filesystem import absolute_path, delete_dir, new_dir, path, resolvable_path, resolve_file
from cppmakelib.utility.version    import Version

class Makefile:
    def           __new__    (cls : type[Makefile], file: resolvable_path = 'make')                                -> Makefile: ...
    def           __init__   (self: Makefile,       file: resolvable_path = 'make')                                -> None    : ...
    async def    __ainit__   (self: Makefile,       file: resolvable_path = 'make')                                -> None    : ...
    def             configure(self: Makefile,       configure_file: path, build_dir: path, build_flags: list[str]) -> None    : ...
    async def async_configure(self: Makefile,       configure_file: path, build_dir: path, build_flags: list[str]) -> None    : ...
    def             build    (self: Makefile,       build_dir: path)                                               -> None    : ...
    async def async_build    (self: Makefile,       build_dir: path)                                               -> None    : ...
    def             install  (self: Makefile,       build_dir: path, install_dir: path)                            -> None    : ...
    async def async_install  (self: Makefile,       build_dir: path, install_dir: path)                            -> None    : ...
    file       : resolvable_path
    version    : Version
    build_flags: list[str]

    async def _async_get_version(self: Makefile) -> Version: ...

makefile: Makefile



@member(Makefile)
@syncable
@unique_on(resolve_file)
async def __ainit__(self: Makefile, file: path = 'make') -> None:
    self.file        = file
    self.version     = await self._async_get_version()
    self.build_flags = [
        f'CXX={compiler.file}',
        f'CXXFLAGS={compiler.compile_flags}'
    ]

@member(Makefile)
@syncable
async def async_configure(
    self          : Makefile, 
    configure_file: path,
    build_dir     : path, 
    build_flags   : list[str], 
) -> None:
    try:
        new_dir(build_dir) # Must configure in a new empty dir.
        await async_run(
            file=configure_file,
            args=[
                *(self.build_flags + build_flags)
            ],
            cwd=build_dir
        )
    except:
        delete_dir(build_dir, not_exist_ok=True)
        raise

@member(Makefile)
@syncable
async def async_build(
    self     : Makefile,
    build_dir: path
) -> None:
    await async_run(
        file=self.file,
        args=[
            '-C', build_dir,
            '-j', str(config.jobs)
        ]
    )

@member(Makefile)
@syncable
async def async_install(
    self       : Makefile,
    build_dir  : path,
    install_dir: path
) -> None:
    try:
        new_dir(install_dir, exist_ok=True)
        await async_run(
            file=self.file,
            args=[
                '-C', build_dir,
                'install'
                '--prefix', absolute_path(install_dir),
                '-j', str(config.jobs)
            ]
        )
    except:
        delete_dir(install_dir, not_exist_ok=True)
        raise

@member(Makefile)
async def _async_get_version(self: Makefile) -> Version:
    try:
        stdout = await async_run(
            file=self.file,
            args=['--version'],
            return_stdout=True
        )
    except SubprocessError as error:
        raise ConfigError(f'makefile check failed (with file = {self.file})') from error
    try:
        version = Version.parse(pattern=r'^GNU Make (\d+)\.(\d+)\.(\d+)', string=stdout.splitlines()[0])
    except Version.ParseError as error:
        raise ConfigError(f'makefile check failed (with file = {self.file})') from error
    if version < 3:
        raise ConfigError(f'makefile version is too old (with file = {self.file}, version = {version}, requires = 3+)')
    return version
        
makefile = Makefile()