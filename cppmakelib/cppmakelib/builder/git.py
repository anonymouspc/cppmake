from cppmakelib.error.config        import ConfigError
from cppmakelib.error.subprocess    import SubprocessError
from cppmakelib.execution.run       import async_run
from cppmakelib.utility.decorator   import member, syncable
from cppmakelib.utility.version     import parse_version

class Git:
    name = "git"
    def           __init__ (self, path="git"): ...
    async def     __ainit__(self, path="git"): ...
    def             log    (self, git_dir):    ...
    async def async_log    (self, git_dir):    ...
    def             status (self, git_dir):    ...
    async def async_status (self, git_dir):    ...

git = ...



@member(Git)
@syncable
async def __ainit__(self, path="git"):
    self.path = path
    self.version = await self._async_get_version()

@member(Git)
@syncable
async def async_log(self, git_dir):
    return await async_run(
        command=[
            self.path,
            "-C", git_dir,
            "log", "-1", "--format=%H"
        ],
        return_stdout=True
    )

@member(Git)
@syncable
async def async_status(self, git_dir):
    return await async_run(
        command=[
            self.path,
            "-C", git_dir,
            "status", "--short"
        ],
        return_stdout=True
    )

@member(Git)
async def _async_get_version(self):
    try:
        version_str = await async_run(command=[self.path, "--version"], return_stdout=True)
        if "git" not in version_str.lower():
            raise ConfigError(f'git is not valid (with "{self.path} --version" outputs "{version_str.replace('\n', ' ')}")')
        return parse_version(version_str)
    except SubprocessError as error:
        raise ConfigError(f'git is not valid (with "{self.path} --version" outputs "{error.stderr.replace('\n', ' ')}" and exits {error.code})')
    except FileNotFoundError as error:
        raise ConfigError(f'git is not found (with "{self.path} --version" fails "{error}")')

git = Git()