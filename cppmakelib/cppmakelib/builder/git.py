from cppmakelib.error.config        import ConfigError
from cppmakelib.error.subprocess    import SubprocessError
from cppmakelib.execution.run       import async_run
from cppmakelib.utility.decorator   import member, syncable

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
    await Git._async_check(path)
    self.path = path

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
            "status"
        ],
        return_stdout=True
    )

@member(Git)
async def _async_check(path):
    try:
        version = await async_run(command=[path, "--version"], return_stdout=True)
        if "git" not in version.lower():
            raise ConfigError(f'git is not valid (with "{path} --version" outputs "{version.replace('\n', ' ')}")')
    except SubprocessError as error:
        raise ConfigError(f'git is not valid (with "{path} --version" outputs "{str(error).replace('\n', ' ')}" and exits {error.code})')
    except FileNotFoundError as error:
        raise ConfigError(f'git is not installed (with "{path} --version" fails "{error}")')

git = Git()