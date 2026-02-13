from cppmakelib.unit.package       import Package, main_package
from cppmakelib.utility.decorator  import member
from cppmakelib.utility.filesystem import change_current_dir, join_path, normal_path, path, relative_path
import typing

class Context:
    def __init__(self, package: Package) -> None                       : ...
    def   switch(self, package: Package) -> typing.ContextManager[None]: ...
    package: Package

    class _ContextManager:
        def __init__ (self, context: Context, package: Package)      -> None: ...
        def __enter__(self)                                          -> None: ...
        def __exit__ (self, *args: typing.Any, **kwargs: typing.Any) -> None: ...
        _context    : Context
        _old_package: Package
        _new_package: Package
        _old_to_new : path
        _new_to_old : path  


context: Context



@member(Context)
def __init__(self: Context, package: Package) -> None:
    self.package = package

@member(Context)
def switch(self: Context, package: Package) -> typing.ContextManager[None]:
    return Context._ContextManager(self, package)

@member(Context._ContextManager)
def __init__(self: Context._ContextManager, context: Context, package: Package) -> None:
    self._context     = context
    self._old_package = context.package
    self._new_package = package

@member(Context._ContextManager)
def __enter__(self: Context._ContextManager) -> None:
    self._context.package = self._new_package
    self._old_to_new = relative_path(from_path=self._old_package.dir, to_path=self._new_package.dir)
    self._new_to_old = relative_path(from_path=self._new_package.dir, to_path=self._old_package.dir)
    change_current_dir(self._old_to_new)
    for package in Package._unique.values():
        for key, value in vars(package):
            if key.endswith('dir') or key.endswith('file'):
                setattr(package, key, normal_path(join_path(self._new_to_old, value))) 

@member(Context._ContextManager)
def __exit__(self: Context._ContextManager, *args: typing.Any, **kwargs: typing.Any) -> None:
    self._context.package = self._old_package
    change_current_dir(self._new_to_old)
    for package in Package._unique.values():
        for key, value in vars(package):
            if key.endswith('dir') or key.endswith('file'):
                setattr(package, key, normal_path(join_path(self._old_to_new, value)))

context = Context(main_package)
