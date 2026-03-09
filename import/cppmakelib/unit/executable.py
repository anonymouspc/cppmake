from cppmakelib.error.subprocess   import SubprocessError
from cppmakelib.executor.run       import async_run
from cppmakelib.executor.scheduler import scheduler
from cppmakelib.utility.decorator  import member, once, pre, syncable, unique_in
from cppmakelib.utility.filesystem import normal_path, path

class Executable:
    def           __new__  (cls : type[Executable], file: path) -> Executable: ...
    def           __init__ (self: Executable,       file: path) -> None      : ...
    def             execute(self: Executable)                   -> None      : ...
    async def async_execute(self: Executable)                   -> None      : ...
    def             test   (self: Executable)                   -> None      : ...
    async def async_test   (self: Executable)                   -> None      : ...



@member(Executable)
@unique_in(context.package)
@pre(1, normal_path)
def __init__(self: Executable, file: path) -> None:
    super(Executable, self).__init__(file)
 
@member(Executable)
@syncable
@once
async def async_execute(self: Executable) -> None:
    async with scheduler.schedule():
        print(f'execute executable {self.file}')
        try:
            await async_run(file=self.file, print_stdout=True, print_stderr=True)
        except SubprocessError:
            pass

@member(Executable)
@syncable
@once
async def async_test(self: Executable) -> None:
    async with scheduler.schedule():
        print(f'test executable {self.file}')
        await async_run(file=self.file, print_stdout=True, print_stderr=True)