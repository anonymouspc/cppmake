from cppmakelib.basic.exit        import on_terminate, rethrow_exception, current_exception
from cppmakelib.utility.decorator import member

@member(KeyboardInterrupt)
def __terminate__():
    try:
        rethrow_exception(current_exception())
    except KeyboardInterrupt:
        exit(-1)

on_terminate(KeyboardInterrupt.__terminate__)