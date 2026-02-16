import asyncio
import functools
import inspect
import typing

def implement  [   **Ts, R](func: typing.Callable[Ts, R])                                     -> typing.Callable[Ts, R]                                                                                         : ...
def lifetime   [   **Ts, R](*variables: typing.Any)                                           -> typing.Callable[[typing.Callable[Ts, R]], typing.Callable[Ts, R]]: ...
def member     [S, **Ts, R](cls: type[S])                                                     -> typing.Callable[[typing.Callable[Ts, R]], typing.Callable[Ts, R]]: ...
def once       [S, **Ts, R](func: typing.Callable[typing.Concatenate[S, Ts], R])              -> typing.Callable[typing.Concatenate[S, Ts], R]                                                                                        : ...
def pre        [   **Ts, R](index: int, operation: typing.Callable[[typing.Any], typing.Any]) -> typing.Callable[[typing.Callable[Ts, R]], typing.Callable[Ts, R]]: ...
def syncable   [   **Ts, R](func: typing.Callable[Ts, R])                                     -> typing.Callable[Ts, R]                                                                                         : ...
def unique     [S, **Ts, R](func: typing.Callable[typing.Concatenate[S, Ts], R])              -> typing.Callable[typing.Concatenate[S, Ts], R]                                                                  : ...
def unique_in  [S, **Ts, R](scope: typing.Any)                                                -> typing.Callable[[typing.Callable[typing.Concatenate[S, Ts], R]], typing.Callable[typing.Concatenate[S, Ts], R]]: ...
def unique_on  [S, **Ts, R](mapping: typing.Callable[Ts, typing.Any])                         -> typing.Callable[[typing.Callable[typing.Concatenate[S, Ts], R]], typing.Callable[typing.Concatenate[S, Ts], R]]: ...



# `@implement`
def implement[**Ts,R](func: typing.Callable[Ts, R]) -> typing.Callable[Ts, R]:
    if inspect.isfunction(func):
        assert hasattr(inspect.getmodule(func), func.__name__)                                                      
        assert str(inspect.signature(getattr(inspect.getmodule(func), func.__name__))) == str(inspect.signature(func)) if getattr(inspect.getmodule(func), func.__name__).__name__ != '_overload_dummy' else True
        setattr(inspect.getmodule(func), func.__name__, func)
        return func
    elif isinstance(func, _MultiFunc):
        for subfunc in func:
            implement(subfunc)
        return implement(func[0])
    else:
        assert False

@implement
def lifetime[**Ts, R](*variables: typing.Any) -> typing.Callable[[typing.Callable[Ts, R]], typing.Callable[Ts, R]]:
    def lifetimizer(func: typing.Callable[Ts, R]) -> typing.Callable[Ts, R]:
        if inspect.isfunction(func):
            setattr(func, '_lifetime', {variable.__name__: variable for variable in variables})
            @functools.wraps(func)
            def lifetime_func(*args: Ts.args, **kwargs: Ts.kwargs) -> R:
                func.__globals__.update(getattr(func, '_lifetime'))
                return func(*args, **kwargs)
            return lifetime_func
        elif isinstance(func, _MultiFunc):
            return _MultiFunc(*[lifetimizer(subfunc) for subfunc in typing.cast(_MultiFunc[Ts, R], func)])
        else:
            assert False
    return lifetimizer

@implement
def member[S, **Ts, R](cls: type[S]) -> typing.Callable[[typing.Callable[Ts, R]], typing.Callable[Ts, R]]:
    def memberizer(func: typing.Callable[Ts, R]) -> typing.Callable[Ts, R]:
        if inspect.isfunction(func):
            assert hasattr(cls, func.__name__)                                         
            assert str(inspect.signature(getattr(cls, func.__name__))) == str(inspect.signature(func)) if getattr(cls, func.__name__).__name__ != '_overload_dummy' else True
            setattr(cls, func.__name__, func)
            return func
        elif isinstance(func, _MultiFunc):
            for subfunc in func:
                memberizer(subfunc)
            def _no_global_callable(*args: ..., **kwargs: ...) -> ...:
                assert False
            return _no_global_callable
        else:
            assert False
    return memberizer

@implement
def once[S, **Ts, R](func: typing.Callable[typing.Concatenate[S, Ts], R]) -> typing.Callable[typing.Concatenate[S, Ts], R]:
    if inspect.isfunction(func) and not inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        def once_func(self: S, *args: Ts.args, **kwargs: Ts.kwargs) -> R:
            arg = _get_arg_tuple((self, ) + args, kwargs, func)[1:] # Use `[1:]` to remove self parameter.
            if not hasattr        (self, '_once'):
                setattr           (self, '_once', {})
            if func not in getattr(self, '_once').keys():
                getattr           (self, '_once')[func] = {}
            if arg not in getattr (self, '_once')[func].keys():
                getattr           (self, '_once')[func][arg] = func(self, *args, **kwargs)
            return getattr        (self, '_once')[func][arg]
        return once_func
    elif inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def once_func(self: S, *args: Ts.args, **kwargs: Ts.kwargs) -> typing.Any:
            arg = _get_arg_tuple((self, ) + args, kwargs, func)[1:] # Use `[1:]` to remove self parameter.
            if not hasattr        (self, '_once'):
                setattr           (self, '_once', {})
            if func not in getattr(self, '_once').keys():
                getattr           (self, '_once')[func] = {}
            if arg not in getattr (self, '_once')[func].keys():
                getattr           (self, '_once')[func][arg] = asyncio.create_task(func(self, *args, **kwargs))
            return await getattr  (self, '_once')[func][arg]
        return typing.cast(typing.Callable[typing.Concatenate[S, Ts], R], once_func)
    elif isinstance(func, _MultiFunc):
        return _MultiFunc(*[once(subfunc) for subfunc in typing.cast(_MultiFunc[typing.Concatenate[S, Ts], R], func)])
    else:
        assert False

@implement
def pre[**Ts, R](index: int, operation: typing.Callable[[typing.Any], typing.Any]) -> typing.Callable[[typing.Callable[Ts, R]], typing.Callable[Ts, R]]:
    def preizer(func: typing.Callable[Ts, R]) -> typing.Callable[Ts, R]:
        if inspect.isfunction(func) and not inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            def pre_func(*args: Ts.args, **kwargs: Ts.kwargs) -> R:
                args, kwargs = _set_index_arg(index, args, kwargs, func, operation)
                return func(*args, **kwargs)
            return pre_func
        elif inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def pre_func(*args: Ts.args, **kwargs: Ts.kwargs) -> typing.Any:
                args, kwargs = _set_index_arg(index, args, kwargs, func, operation)
                return await func(*args, **kwargs)
            return typing.cast(typing.Callable[Ts, R], pre_func)
        elif isinstance(func, _MultiFunc):
            return _MultiFunc(*[preizer(subfunc) for subfunc in typing.cast(_MultiFunc[Ts, R], func)])
        else:
            assert False
    return preizer

@implement
def syncable[**Ts, R](func: typing.Callable[Ts, R]) -> typing.Callable[Ts, R]:
    if inspect.isfunction(func) and not inspect.iscoroutinefunction(func):
        return func
    elif inspect.iscoroutinefunction(func):
        assert func.__name__.startswith('async_') or func.__name__.startswith('__a')
        @_resignature_remove_async(func)
        @functools.wraps(func)
        def sync_func(*args: Ts.args, **kwargs: Ts.kwargs) -> typing.Any:
            from cppmakelib.executor.operation import sync_wait
            return sync_wait(func(*args, **kwargs))
        return _MultiFunc(typing.cast(typing.Callable[Ts, R], func), sync_func)
    elif isinstance(func, _MultiFunc):
        return _MultiFunc(*[syncable(subfunc) for subfunc in typing.cast(_MultiFunc[Ts, R], func)])
    else:
        assert False

@implement
def unique[S, **Ts, R](func: typing.Callable[typing.Concatenate[S, Ts], R]) -> typing.Callable[typing.Concatenate[S, Ts], R]:
    if inspect.isfunction(func):
        assert func.__name__ == '__init__' or func.__name__ == '__ainit__'
        @_resignature_init_to_new(func)
        @functools.wraps(func)
        def unique_func(cls: type[S], *args: Ts.args, **kwargs: Ts.kwargs) -> S:
            arg = _get_arg_tuple((None, ) + args, kwargs, func)[1:] # Use `None` to stub `self`, and use `[1:]` to remove self parameter.
            if not hasattr       (cls, '_unique'):
                setattr          (cls, '_unique', {})
            if arg not in getattr(cls, '_unique').keys():
                getattr          (cls, '_unique')[arg] = object.__new__(cls)
            return getattr       (cls, '_unique')[arg]
        unique_func.__name__ = '__new__'
        return _MultiFunc(func, unique_func)
    elif isinstance(func, _MultiFunc):
        return _MultiFunc(*[unique(subfunc) for subfunc in typing.cast(_MultiFunc[typing.Concatenate[S, Ts], R], func)])
    else:
        assert False

@implement
def unique_in[S, **Ts, R](scope: typing.Any) -> typing.Callable[[typing.Callable[typing.Concatenate[S, Ts], R]], typing.Callable[typing.Concatenate[S, Ts], R]]:
    def uniquizer(func: typing.Callable[typing.Concatenate[S, Ts], R]) -> typing.Callable[typing.Concatenate[S, Ts], R]:
        if inspect.isfunction(func):
            assert func.__name__ == '__init__' or func.__name__ == '__ainit__'
            @_resignature_init_to_new(func)
            @functools.wraps(func)
            def unique_func(cls: type[S], *args: Ts.args, **kwargs: Ts.kwargs) -> S:
                arg = _get_arg_tuple((None, ) + args, kwargs, func) # Use `None` to stub `self`, and use `[1:]` to remove self parameter.
                if not hasattr       (scope, '_unique_in'):
                    setattr          (scope, '_unique_in', {})
                if cls not in getattr(scope, '_unique_in').keys():
                    getattr          (scope, '_unique_in')[cls] = {}
                if arg not in getattr(scope, '_unique_in')[cls].keys():
                    getattr          (scope, '_unique_in')[cls][arg] = object.__new__(cls)
                return getattr       (scope, '_unique_in')[cls][arg]
            unique_func.__name__ = '__new__'
            return _MultiFunc(func, unique_func)
        elif isinstance(func, _MultiFunc):
            return _MultiFunc(*[uniquizer(subfunc) for subfunc in typing.cast(_MultiFunc[typing.Concatenate[S, Ts], R], func)])
        else:
            assert False
    return uniquizer

@implement             
def unique_on[S, **Ts, R](mapping: typing.Callable[Ts, typing.Any]) -> typing.Callable[[typing.Callable[typing.Concatenate[S, Ts], R]], typing.Callable[typing.Concatenate[S, Ts], R]]:
    def uniquizer(func: typing.Callable[typing.Concatenate[S, Ts], R]) -> typing.Callable[typing.Concatenate[S, Ts], R]:
        if inspect.isfunction(func):
            assert func.__name__ == '__init__' or func.__name__ == '__ainit__'
            @_resignature_init_to_new(func)
            @functools.wraps(func)
            def unique_func(cls: type, *args: Ts.args, **kwargs: Ts.kwargs) -> S:
                if not hasattr                            (cls, '_unique_on'):
                    setattr                               (cls, '_unique_on', {})
                if mapping not in                  getattr(cls, '_unique_on').keys():
                    getattr                               (cls, '_unique_on')[mapping] = {}
                if mapping(*args, **kwargs) not in getattr(cls, '_unique_on')[mapping].keys():
                    getattr                               (cls, '_unique_on')[mapping][mapping(*args, **kwargs)] = object.__new__(cls)
                return getattr                            (cls, '_unique_on')[mapping][mapping(*args, **kwargs)]
            unique_func.__name__ = '__new__'
            return _MultiFunc(typing.cast(typing.Callable[typing.Concatenate[S, Ts], R], once(func)), unique_func)
        elif isinstance(func, _MultiFunc):
            return _MultiFunc(*[uniquizer(subfunc) for subfunc in typing.cast(_MultiFunc[typing.Concatenate[S, Ts], R], func)])
        else:
            assert False
    return uniquizer

class _MultiFunc[**Ts, R]:
    def __init__   (self: _MultiFunc[Ts, R], first: typing.Callable[Ts, R], *other: ...) -> None                                                : ... # type: ignore
    def __call__   (self: _MultiFunc[Ts, R], *args: Ts.args, **kwargs: Ts.kwargs)        -> R                                                   : ...
    def __iter__   (self: _MultiFunc[Ts, R])                                             -> typing.Iterator[typing.Callable[Ts, R] | typing.Any]: ...
    @typing.overload
    def __getitem__(self: _MultiFunc[Ts, R], index: typing.Literal[0])                   -> typing.Callable[Ts, R]                              : ...
    @typing.overload
    def __getitem__(self: _MultiFunc[Ts, R], index: slice)                               -> typing.Iterable[typing.Any]                         : ...

    _functions: tuple[typing.Callable[Ts, R], ...]

@member(_MultiFunc)
def __init__[**Ts, R](self: _MultiFunc[Ts, R], first: typing.Callable[Ts, R], *other: ...) -> None:
    self._functions = (first, *other)

@member(_MultiFunc)
def __call__[**Ts, R](self: _MultiFunc[Ts, R], *args: Ts.args, **kwargs: Ts.kwargs) -> R:
    return self._functions[0](*args, **kwargs)

@member(_MultiFunc)
def __iter__[**Ts, R](self: _MultiFunc[Ts, R]) -> typing.Iterator[typing.Callable[Ts, R] | typing.Any]:
    return iter(self._functions)

@member(_MultiFunc)
def __getitem__[**Ts, R](self: _MultiFunc[Ts, R], index: typing.Literal[0] | slice) -> typing.Callable[Ts, R] | typing.Iterable[typing.Any]:
    return self._functions[index]

def _get_arg_tuple(args: tuple[typing.Any, ...], kwargs: dict[str, typing.Any], func: typing.Callable[..., typing.Any]) -> tuple[typing.Any, ...]:
    params = {param: value.default for param, value in inspect.signature(func).parameters.items()}
    for index, param in enumerate(params.keys()):
        if index < len(args):
            params[param] = args[index]
        elif param in kwargs.keys():
            params[param] = kwargs[param]
    return tuple(params.values())

def _set_index_arg(index: int, args: tuple[typing.Any, ...], kwargs: dict[str, typing.Any], func: typing.Callable[..., typing.Any], operation: typing.Callable[[typing.Any], typing.Any]) -> tuple[typing.Any, ...]:
    params = {param: value.default for param, value in inspect.signature(func).parameters.items()}
    if index < len(args):
        return args[:index] + (operation(args[index]), ) + args[index+1:], kwargs
    else:
        params = [(param, value.default) for param, value in inspect.signature(func).parameters.items()]
        param, default = params[index]
        if param in kwargs.keys():
            kwargs[param] = operation(kwargs[param])
        else:
            kwargs[param] = operation(default)
        return args, kwargs

def _resignature_remove_async[**Ts, R](wrapped: typing.Callable[Ts, typing.Awaitable[R]]) -> typing.Callable[[typing.Callable[Ts, R]], typing.Callable[Ts, R]]:
    def resigner(func: typing.Callable[Ts, R]) -> typing.Callable[Ts, R]:
        func.__name__     = wrapped.__name__    .removeprefix('async_') if wrapped.__name__    .startswith('async_') else '__' + wrapped.__name__    .removeprefix('__a')
        func.__qualname__ = wrapped.__qualname__.removeprefix('async_') if wrapped.__qualname__.startswith('async_') else '__' + wrapped.__qualname__.removeprefix('__a')
        return func
    return resigner

def _resignature_init_to_new[S, **Ts](wrapped: typing.Callable[typing.Concatenate[S, Ts], None]) -> typing.Callable[[typing.Callable[typing.Concatenate[type[S], Ts], S]], typing.Callable[typing.Concatenate[type[S], Ts], S]]:
    def resigner(func: typing.Callable[typing.Concatenate[type[S], Ts], S]) -> typing.Callable[typing.Concatenate[type[S], Ts], S]:
        func.__name__      = '__new__'
        func.__qualname__  = '__new__'
        params    : dict[str, inspect.Parameter] = inspect.signature(wrapped).parameters.copy()
        cls       : type                         = params['self'].annotation
        cls_param : inspect.Parameter            = inspect.Parameter('cls', inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=type[cls])
        arg_params: list[inspect.Parameter]      = list(params.values())[1:]
        signature : inspect.Signature            = inspect.Signature(parameters=[cls_param] + arg_params, return_annotation=cls)
        setattr(func, '__signature__', signature)
        return func
    return resigner
