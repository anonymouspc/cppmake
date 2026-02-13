import asyncio
import threading
import typing

def sync_wait     [T](task :      typing.Awaitable[T] ) -> T      : ...
def start_detached[T](task :      typing.Awaitable[T] ) -> None   : ...
def when_all      [T](tasks: list[typing.Awaitable[T]]) -> list[T]: ...
def when_any      [T](tasks: list[typing.Awaitable[T]]) -> T      : ...



def sync_wait[T](task: typing.Awaitable[T]) -> T:
    try:
        asyncio.get_running_loop()
        in_event_loop = True
    except RuntimeError:
        in_event_loop = False

    if not in_event_loop:
        return _sync_run(task)
    else:
        value: tuple[T]      | None = None
        error: BaseException | None = None
        def sync_func():
            try:
                nonlocal value
                value = (_sync_run(task), )
            except BaseException as base_error:
                nonlocal error
                error = base_error
        thread = threading.Thread(target=sync_func)
        thread.start()
        thread.join()
        if error is None:
            assert value is not None
            return value[0]
        else: 
            raise error

async def when_all[T](tasks: list[typing.Awaitable[T]]) -> list[T]:
    return await asyncio.gather(*tasks)

def _sync_run[T](awaitable: typing.Awaitable[T]) -> T:
    async def _async_run() -> T:
        return await awaitable
    return asyncio.run(_async_run())