from cppmakelib.executor.operation import sync_wait
import asyncio
import inspect
import typing

def implement  [   **Ts, R](func: typing.Callable[Ts, R])                        -> typing.Callable[Ts, R]                                                                                         : ...
def lifetime   [S, **Ts, R](*variables: typing.Any)                              -> typing.Callable[[typing.Callable[typing.Concatenate[S, Ts], R]], typing.Callable[typing.Concatenate[S, Ts], R]]: ...
def member     [S, **Ts, R](cls: type)                                           -> typing.Callable[[typing.Callable[typing.Concatenate[S, Ts], R]], typing.Callable[typing.Concatenate[S, Ts], R]]: ...
def once       [S,       R](func: typing.Callable[[S], R])                       -> typing.Callable[[S], R]                                                                                        : ...
def pre        [S, **Ts, R](mapping: typing.Callable[[typing.Any], typing.Any])  -> typing.Callable[[typing.Callable[typing.Concatenate[S, Ts], R]], typing.Callable[typing.Concatenate[S, Ts], R]]: ...
def post       [S, **Ts, R](mapping: typing.Callable[[R], R])                    -> typing.Callable[[typing.Callable[typing.Concatenate[S, Ts], R]], typing.Callable[typing.Concatenate[S, Ts], R]]: ...
def syncable   [   **Ts, R](func: typing.Callable[Ts, typing.Awaitable[R]])      -> typing.Callable[Ts, typing.Awaitable[R]]                                                                       : ...
def unique     [S, **Ts, R](func: typing.Callable[typing.Concatenate[S, Ts], R]) -> typing.Callable[typing.Concatenate[S, Ts], R]                                                                  : ...
def unique_in  [S, **Ts, R](scope: typing.Any)                                   -> typing.Callable[[typing.Callable[typing.Concatenate[S, Ts], R]], typing.Callable[typing.Concatenate[S, Ts], R]]: ...
def unique_on  [S, **Ts, R](mapping: typing.Callable[Ts, typing.Any])            -> typing.Callable[[typing.Callable[typing.Concatenate[S, Ts], R]], typing.Callable[typing.Concatenate[S, Ts], R]]: ...



def implement[**Ts,R](func: typing.Callable[Ts, R]) -> typing.Callable[Ts, R]:
    if inspect.isfunction(func):
        assert hasattr(inspect.getmodule(func), func.__name__) 
        assert inspect.signature(getattr(inspect.getmodule(func), func.__name__)) == inspect.signature(func)
        setattr(inspect.getmodule(func), func.__name__, func)
        return func
    elif isinstance(func, _MultiFunc):
        for subfunc in typing.cast(_MultiFunc[Ts, R], func):
            implement(subfunc)
        return typing.cast(_MultiFunc[Ts, R], func)
    else:
        assert False

def lifetime[S, **Ts, R](*variables: typing.Any) -> typing.Callable[[typing.Callable[typing.Concatenate[S, Ts], R]], typing.Callable[typing.Concatenate[S, Ts], R]]:
    def lifetimizer(func: typing.Callable[typing.Concatenate[S, Ts], R]) -> typing.Callable[typing.Concatenate[S, Ts], R]:
        if inspect.isfunction(func):
            setattr(func, '_lifetime', {variable.__name__: variable for variable in variables})
            def lifetime_func(self: S, *args: Ts.args, **kwargs: Ts.kwargs) -> R:
                func.__globals__.update(getattr(func, '_lifetime'))
                return func(self, *args, **kwargs)
            lifetime_func.__name__ = func.__name__
            return lifetime_func
        elif isinstance(func, _MultiFunc):
            return _MultiFunc(*[lifetimizer(subfunc) for subfunc in typing.cast(_MultiFunc[typing.Concatenate[S, Ts], R], func)])
        else:
            assert False
    return lifetimizer

def member[S, **Ts, R](cls: type) -> typing.Callable[[typing.Callable[typing.Concatenate[S, Ts], R]], typing.Callable[typing.Concatenate[S, Ts], R]]:
    def memberizer(func: typing.Callable[typing.Concatenate[S, Ts], R]) -> typing.Callable[typing.Concatenate[S, Ts], R]:
        if inspect.isfunction(func):
            assert hasattr(cls, func.__name__) 
            assert inspect.signature(getattr(cls, func.__name__)) == inspect.signature(func) if not hasattr(cls, '__parameters__') else True
            setattr(cls, func.__name__, func)
            return func
        elif isinstance(func, _MultiFunc):
            for subfunc in typing.cast(_MultiFunc[typing.Concatenate[S, Ts], R], func):
                memberizer(subfunc)
            return typing.cast(_MultiFunc[typing.Concatenate[S, Ts], R], func)
        else:
            assert False
    return memberizer

def once[S, R](func: typing.Callable[[S], R]) -> typing.Callable[[S], R]:
    if inspect.isfunction(func) and not inspect.iscoroutinefunction(func):
        def once_func(self: S) -> R:
            if not hasattr      (self, f'_once_{func.__name__}'):
                setattr         (self, f'_once_{func.__name__}', ())
            if getattr          (self, f'_once_{func.__name__}') == ():
                setattr         (self, f'_once_{func.__name__}', (func(self), ))
            return getattr      (self, f'_once_{func.__name__}')[0]
        once_func.__name__ = func.__name__
        return once_func
    elif inspect.iscoroutinefunction(func):
        async def once_func(self: S) -> typing.Any:
            if not hasattr      (self, f'_once_{func.__name__}'):
                setattr         (self, f'_once_{func.__name__}', asyncio.create_task(func(self)))
            return await getattr(self, f'_once_{func.__name__}')
        once_func.__name__ = func.__name__
        return typing.cast(typing.Callable[[S], R], once_func)
    elif isinstance(func, _MultiFunc):
        return _MultiFunc(*[once(subfunc) for subfunc in typing.cast(_MultiFunc[[S], R], func)])
    else:
        assert False

def pre[S, **Ts, R](mapping: typing.Callable[[typing.Any], typing.Any]) -> typing.Callable[[typing.Callable[typing.Concatenate[S, Ts], R]], typing.Callable[typing.Concatenate[S, Ts], R]]:
    def preizer(func: typing.Callable[typing.Concatenate[S, Ts], R]) -> typing.Callable[typing.Concatenate[S, Ts], R]:
        if inspect.isfunction(func) and not inspect.iscoroutinefunction(func):
            def pre_func(self: S, *args: Ts.args, **kwargs: Ts.kwargs) -> R:
                args, kwargs = _set_first_arg(args, kwargs, func, mapping)
                return func(self, *args, **kwargs)
            pre_func.__name__ = func.__name__
            return pre_func
        elif inspect.iscoroutinefunction(func):
            async def pre_func(self: S, *args: Ts.args, **kwargs: Ts.kwargs) -> typing.Any:
                args, kwargs = _set_first_arg(args, kwargs, func, mapping)
                return await func(self, *args, **kwargs)
            pre_func.__name__ = func.__name__
            return typing.cast(typing.Callable[typing.Concatenate[S, Ts], R], pre_func)
        elif isinstance(func, _MultiFunc):
            return _MultiFunc(*[preizer(subfunc) for subfunc in typing.cast(_MultiFunc[typing.Concatenate[S, Ts], R], func)])
        else:
            assert False
    return preizer

def syncable[**Ts, R](func: typing.Callable[Ts, typing.Awaitable[R]]) -> typing.Callable[Ts, typing.Awaitable[R]]:
    if inspect.iscoroutinefunction(func):
        assert func.__name__.startswith('async_') or func.__name__.startswith('__a')
        def sync_func(*args: Ts.args, **kwargs: Ts.kwargs) -> R:
            return sync_wait(func(*args, **kwargs))
        sync_func.__name__ = func.__name__.removeprefix('async_') if func.__name__.startswith('async_') else func.__name__.replace('__a', '__')
        return _MultiFunc(func, sync_func)
    elif isinstance(func, _MultiFunc):
        return _MultiFunc(*[syncable(subfunc) for subfunc in typing.cast(_MultiFunc[Ts, typing.Awaitable[R]], func)])
    else:
        assert False

def unique[S, **Ts, R](func: typing.Callable[typing.Concatenate[S, Ts], R]) -> typing.Callable[typing.Concatenate[S, Ts], R]:
    if inspect.isfunction(func) and not inspect.iscoroutinefunction(func):
        assert func.__name__ == '__init__'
        def unique_func(cls: type, *args: Ts.args, **kwargs: Ts.kwargs) -> S:
            arg = _get_arg_tuple(args, kwargs, func)
            if not hasattr       (cls, '_unique'):
                setattr          (cls, '_unique', {})
            if arg not in getattr(cls, '_unique').keys():
                getattr          (cls, '_unique')[arg] = object.__new__(cls)
            return getattr       (cls, '_unique')[arg]
        unique_func.__name__ = '__new__'
        return _MultiFunc(func, unique_func)
    elif inspect.iscoroutinefunction(func):
        assert func.__name__ == '__ainit__'
        async def unique_func(cls: type, *args: Ts.args, **kwargs: Ts.kwargs) -> typing.Any:
            arg = _get_arg_tuple(args, kwargs, func)
            if not hasattr       (cls, '_unique'):
                setattr          (cls, '_unique', {})
            if arg not in getattr(cls, '_unique').keys():
                getattr          (cls, '_unique')[arg] = object.__new__(cls)
            await getattr        (cls, '_unique')[arg].__ainit__(*args, **kwargs)
            return getattr       (cls, '_unique')[arg]
        unique_func.__name__  = '__anew__'
        return _MultiFunc(typing.cast(typing.Callable[typing.Concatenate[S, Ts], R], func), unique_func)
    elif isinstance(func, _MultiFunc):
        return _MultiFunc(*[unique(subfunc) for subfunc in typing.cast(_MultiFunc[typing.Concatenate[S, Ts], R], func)])
    else:
        assert False

def unique_in[S, **Ts, R](scope: typing.Any) -> typing.Callable[[typing.Callable[typing.Concatenate[S, Ts], R]], typing.Callable[typing.Concatenate[S, Ts], R]]:
    def uniquizer(func: typing.Callable[typing.Concatenate[S, Ts], R]) -> typing.Callable[typing.Concatenate[S, Ts], R]:
        if inspect.isfunction(func) and not inspect.iscoroutinefunction(func):
            assert func.__name__ == '__init__'
            def unique_func(cls: type, *args: Ts.args, **kwargs: Ts.kwargs) -> S:
                arg = _get_arg_tuple(args, kwargs, func)
                if not hasattr       (scope, '_unique_in'):
                    setattr          (scope, '_unique_in', {})
                if cls not in getattr(scope, '_unique_in').keys():
                    getattr          (scope, '_unique_in')[cls] = {}
                if arg not in getattr(scope, '_unique_in')[cls].keys():
                    getattr          (scope, '_unique_in')[cls][arg] = object.__new__(cls)
                return getattr       (scope, '_unique_in')[cls][arg]
            unique_func.__name__ = '__new__'
            return _MultiFunc(func, unique_func)
        elif inspect.iscoroutinefunction(func):
            assert func.__name__ == '__ainit__'
            async def unique_func(cls: type, *args: Ts.args, **kwargs: Ts.kwargs) -> typing.Any:
                arg = _get_arg_tuple(args, kwargs, func)
                if not hasattr       (scope, '_unique_in'):
                    setattr          (scope, '_unique_in', {})
                if cls not in getattr(scope, '_unique_in').keys():
                    getattr          (scope, '_unique_in')[cls] = {}
                if arg not in getattr(scope, '_unique_in')[cls].keys():
                    getattr          (scope, '_unique_in')[cls][arg] = object.__new__(cls)
                await getattr        (scope, '_unique_in')[cls][arg].__ainit__(*args, **kwargs)
                return getattr       (scope, '_unique_in')[cls][arg]
            unique_func.__name__ = '__anew__'
            return _MultiFunc(typing.cast(typing.Callable[typing.Concatenate[S, Ts], R], func), unique_func)
        elif isinstance(func, _MultiFunc):
            return _MultiFunc(*[uniquizer(subfunc) for subfunc in typing.cast(_MultiFunc[typing.Concatenate[S, Ts], R], func)])
        else:
            assert False
    return uniquizer
                    
def unique_on[S, **Ts, R](mapping: typing.Callable[Ts, typing.Any]) -> typing.Callable[[typing.Callable[typing.Concatenate[S, Ts], R]], typing.Callable[typing.Concatenate[S, Ts], R]]:
    def uniquizer(func: typing.Callable[typing.Concatenate[S, Ts], R]) -> typing.Callable[typing.Concatenate[S, Ts], R]:
        if inspect.isfunction(func) and not inspect.iscoroutinefunction(func):
            assert func.__name__ == '__init__'
            def unique_func(cls: type, *args: Ts.args, **kwargs: Ts.kwargs) -> S:
                if not hasattr                            (cls, '_unique_on'):
                    setattr                               (cls, '_unique_on', {})
                if mapping not in                  getattr(cls, '_unique_on').keys():
                    getattr                               (cls, '_unique_on')[mapping] = {}
                if mapping(*args, **kwargs) not in getattr(cls, '_unique_on')[mapping].keys():
                    getattr                               (cls, '_unique_on')[mapping][mapping(*args, **kwargs)] = object.__new__(cls)
                return getattr                            (cls, '_unique_on')[mapping][mapping(*args, **kwargs)]
            unique_func.__name__ = '__new__'
            return _MultiFunc(func, unique_func)
        elif inspect.iscoroutinefunction(func):
            assert func.__name__ == '__ainit__'
            async def unique_func(cls: type, *args: Ts.args, **kwargs: Ts.kwargs) -> typing.Any:
                if not hasattr                            (cls, '_unique_on'):
                    setattr                               (cls, '_unique_on', {})
                if mapping not in                  getattr(cls, '_unique_on').keys():
                    getattr                               (cls, '_unique_on')[mapping] = {}
                if mapping(*args, **kwargs) not in getattr(cls, '_unique_on')[mapping].keys():
                    getattr                               (cls, '_unique_on')[mapping][mapping(*args, **kwargs)] = object.__new__(cls)
                await getattr                             (cls, '_unique_on')[mapping][mapping(*args, **kwargs)].__ainit__(*args, **kwargs)
                return getattr                            (cls, '_unique_on')[mapping][mapping(*args, **kwargs)]
            unique_func.__name__ = '__anew__'
            return _MultiFunc(typing.cast(typing.Callable[typing.Concatenate[S, Ts], R], func), unique_func)
        elif isinstance(func, _MultiFunc):
            return _MultiFunc(*[uniquizer(subfunc) for subfunc in typing.cast(_MultiFunc[typing.Concatenate[S, Ts], R], func)])
        else:
            assert False
    return uniquizer

class _MultiFunc[**Ts, R]:
    def __init__(self: _MultiFunc[Ts, R], first: typing.Callable[Ts, R], *other: ...) -> None: ...
    def __call__(self: _MultiFunc[Ts, R], *args: Ts.args, **kwargs: Ts.kwargs)        -> R   : ...
    def __iter__(self: _MultiFunc[Ts, R])                                             -> typing.Iterator[typing.Callable[Ts, R] | typing.Any]: ...

    _functions: tuple[typing.Callable[Ts, R], ...]

@member(_MultiFunc)
def __init__[**Ts, R](self: _MultiFunc[Ts, R], first: typing.Callable[Ts, R], *other: ...) -> None:
    self._functions = (first, *other)

@member(_MultiFunc)
def __call__[**Ts, R](self: _MultiFunc[Ts, R], *args: Ts.args, **kwargs: Ts.kwargs) -> R:
    return self._functions[0](*args, **kwargs)

@member(_MultiFunc)
def __iter__[**Ts, R](self: _MultiFunc[Ts, R]) -> typing.Iterable[typing.Callable[Ts, R] | typing.Any]:
    return iter(self._functions)

def _get_arg_tuple(args: tuple[typing.Any, ...], kwargs: dict[str, typing.Any], func: typing.Callable[..., typing.Any]) -> tuple[typing.Any, ...]:
    params = {param: value.default for param, value in inspect.signature(func).parameters.items()}
    for index, key in enumerate(params.keys()):
        if index < len(args):
            params[key] = args[index]
        elif key in kwargs.keys():
            params[key] = kwargs[key]
    return tuple(params.values())

def _set_first_arg(args: tuple[typing.Any, ...], kwargs: dict[str, typing.Any], func: typing.Callable[..., typing.Any], mapping: typing.Callable[[typing.Any], typing.Any]) -> tuple[typing.Any, ...]:
    if len(args) >= 1:
        return (mapping(args[0]), ) + args[1:], kwargs
    else:
        params = {param: value.default for param, value in inspect.signature(func).parameters.items()}
        for index, key in enumerate(params.keys()):
            if index == 0:
                params[key] = mapping(kwargs[key])
            else:
                params[key] = kwargs[key]
        return args, params
