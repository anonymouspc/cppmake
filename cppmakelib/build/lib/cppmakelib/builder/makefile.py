from cppmakelib.basic.config       import config
from cppmakelib.compiler.all       import compiler
from cppmakelib.error.config       import ConfigError
from cppmakelib.error.subprocess   import SubprocessError
from cppmakelib.execution.run      import async_run
from cppmakelib.file.file_system   import absolute_path, create_dir, remove_dir
from cppmakelib.system.all         import system
from cppmakelib.utility.decorator  import member, syncable
from cppmakelib.utility.version    import parse_version

class Makefile:
    name = "makefile"
    def           __init__(self, path="make"):                        ...
    async def    __ainit__(self, path="make"):                        ...
    def             build (self, package, file="configure", args=[]): ...
    async def async_build (self, package, file="configure", args=[]): ...

makefile = ...



@member(Makefile)
@syncable
async def __ainit__(self, path="make"):
    self.path = path
    self.version = await self._async_get_version()

@member(Makefile)
@syncable
async def async_build(self, package, file="configure", args=[]):
    try:
        create_dir(package.build_dir)
        await async_run(
            command=[
               f"{package.git_dir}/{file}",
               f"CXX={compiler.path}",
               f"CXXFLAGS={' '.join(compiler.compile_flags + package.compile_flags)}"
               f"--prefix={absolute_path(package.install_dir)}",
               f"--libdir={absolute_path(package.install_dir)}/lib"
               *args
            ],
            cwd=package.build_dir
        )
    except:
        remove_dir(package.build_dir)
        raise
    try:
        await async_run(
            command=[
                self.path,
               f"CXX={compiler.path}",
               f"CXXFLAGS={' '.join(compiler.compile_flags + package.compile_flags)}"
                "-C", package.build_dir,
                "-j", str(config.parallel)
            ]
        )
    except:
        raise
    try:
        create_dir(package.install_dir)
        await async_run(
            command=[
                self.path, "install"
                "-C", package.build_dir,
                "-j", str(config.parallel)
            ]
        )
    except:
        remove_dir(package.install_dir)
        raise

@member(Makefile)
async def _async_get_version(self):
    try:
        version_str = await async_run(command=[self.path, "--version"], return_stdout=True)
        if "make" not in version_str.lower():
            raise ConfigError(f'makefile is not valid (with f"{self.path} --version" outputs "{version_str.replace('\n', ' ')}")')
        return parse_version(version_str)
    except SubprocessError as error:
        raise ConfigError(f'makefie is not valid (with f"{self.path} --version" outputs "{error.stderr.replace('\n', ' ')}" and exits exits {error.code})')
    except FileNotFoundError as error:
        raise ConfigError(f'makefile is not found (with f"{self.path} --version" fails "{error}")')
        
makefile = Makefile()