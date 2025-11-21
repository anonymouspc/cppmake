from cppmakelib.basic.config       import config
from cppmakelib.error.config       import ConfigError
from cppmakelib.error.subprocess   import SubprocessError
from cppmakelib.execution.run      import async_run
from cppmakelib.file.file_system   import parent_path, create_dir, remove_dir
from cppmakelib.utility.algorithm  import recursive_collect
from cppmakelib.utility.decorator  import member, syncable

class Cmake:
    name = "cmake"
    def           __init__(self, path="cmake"):              ...
    async def    __ainit__(self, path="cmake"):              ...
    def             build (self, package, dir=".", args=[]): ...
    async def async_build (self, package, dir=".", args=[]): ...

cmake = ...



@member(Cmake)
@syncable
async def __ainit__(self, path="cmake"):
    await Cmake._async_check(path)
    self.path = path

@member(Cmake)
@syncable
async def async_build(self, package, dir=".", args=[]):
    try:
        create_dir(package.build_dir)
        await async_run(
            command=[
                self.path,
                "-S", package.git_dir,
                "-B", package.build_dir,
               f"-DCMAKE_BUILD_TYPE={config.type}",
               f"-DCMAKE_PREFIX_PATH={';'.join(recursive_collect(package, next=lambda package: package.import_packages, collect=lambda package: package.install_dir, root=False))}",
               f"-DCMAKE_INSTALL_PREFIX={package.install_dir}",
                "-DCMAKE_INSTALL_LIBDIR=lib",
               *args
            ]
        )
    except:
        remove_dir(package.build_dir)
        raise
    try:
        await async_run(
            command=[
                self.path,
                "--build", package.build_dir,
                "-j",      str(config.parallel)
            ]
        )
    except:
        raise
    try:
        create_dir(package.install_dir)
        await async_run(
            command=[
                self.path,
                "--install", package.build_dir,
                "-j",        str(config.parallel)
            ]
        )
    except:
        remove_dir(package.install_dir)
        raise

@member(Cmake)
async def _async_check(path):
    try:
        version = await async_run(command=[path, "--version"], return_stdout=True)
        if "cmake" not in version.lower():
            raise ConfigError(f'cmake is not valid (with "{path} --version" outputs "{version.replace('\n', ' ')}")')
    except SubprocessError as error:
        raise ConfigError(f'cmake is not valid (with "{path} --version" outputs "{str(error).replace('\n', ' ')}" and exits {error.code})')
    except FileNotFoundError as error:
        raise ConfigError(f'cmake is not installed (with "{path} --version" fails "{error}")')

cmake = Cmake()
