from cppmakelib.package.basic      import Package
from cppmakelib.package.main       import MainPackage
from cppmakelib.utility.decorator  import member
from cppmakelib.utility.filesystem import change_current_dir, join_path, normal_path, path, relative_path
import typing

class Context:
    def default(self: Context)                   -> typing.ContextManager[None]: ...
    def switch (self: Context, package: Package) -> typing.ContextManager[None]: ...
    package: Package = MainPackage.__new__(MainPackage) # Only `__new__` and do not `__init__`, due to initialize cycle `main_package` -> `import_module('cppmake.py')` -> `Package('boost')` -> `context.default()` -> `main_package`.

    class _ContextManager:
        def __init__ (self: Context._ContextManager, context: Context, package: Package)      -> None: ...
        def __enter__(self: Context._ContextManager)                                          -> None: ...
        def __exit__ (self: Context._ContextManager, *args: typing.Any, **kwargs: typing.Any) -> None: ...
        _context    : Context
        _old_package: Package
        _new_package: Package
        _old_to_new : path
        _new_to_old : path  
    _history: set[Package] = set()

context: Context



@member(Context)
def default(self: Context) -> typing.ContextManager[None]:
    self._history.add(MainPackage.__new__(MainPackage))
    return Context._ContextManager(self, MainPackage.__new__(MainPackage))

@member(Context)
def switch(self: Context, package: Package) -> typing.ContextManager[None]:
    self._history.add(package)
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
    for package in self._context._history:
        for key, value in vars(package).items():
            if key.endswith('dir') or key.endswith('file'):
                setattr(package, key, normal_path(join_path(self._new_to_old, value))) 

@member(Context._ContextManager)
def __exit__(self: Context._ContextManager, *args: typing.Any, **kwargs: typing.Any) -> None:
    self._context.package = self._old_package
    change_current_dir(self._new_to_old)
    for package in self._context._history:
        for key, value in vars(package).items():
            if key.endswith('dir') or key.endswith('file'):
                setattr(package, key, normal_path(join_path(self._old_to_new, value)))

context = Context()
