import typing

@typing.overload
def recursive_collect[T, U, R](node: U, next: typing.Callable[[U | T], list[T]], collect: typing.Callable[[T], R | None], *, flatten: typing.Literal[False] = False) -> list[R]: ...
@typing.overload
def recursive_collect[T, U, R](node: U, next: typing.Callable[[U | T], list[T]], collect: typing.Callable[[T], list[R]],  *, flatten: typing.Literal[True])          -> list[R]: ...



# Our goal is to make the caller more pretty (with the algorithm itself to be maybe dirty).
# Feel free to overwrite the implemention when we need something new from it.

def recursive_collect[T, U, R](
    node   : U, 
    next   : typing.Callable[[U | T], list[T]], 
    collect: typing.Callable[[T], R | list[R] | None], 
    flatten: bool = False
) -> list[R]:
   return _recursive_collect_impl_root(node=node, next=next, collect=collect, flatten=flatten)

def _recursive_collect_impl_root[T, U, R](
    node     : U,
    next     : typing.Callable[[U | T], list[T]],
    collect  : typing.Callable[[T], R | list[R] | None],
    flatten  : bool
) -> list[R]:
    visited  = set[T]()
    collected= list[R]()
    for subnode in next(node):
        _recursive_collect_impl_branch(node=subnode, next=next, collect=collect, flatten=flatten, visited=visited, collected=collected)
    return collected

def _recursive_collect_impl_branch[T, R](
    node     : T,
    next     : typing.Callable[[T], list[T]],
    collect  : typing.Callable[[T], R | list[R] | None],
    flatten  : bool,
    visited  : set[T],
    collected: list[R]
) -> None:
    if node not in visited:
        visited |= {node}
        value = collect(node)
        if value is not None and value not in collected:
            if not flatten:
                assert not isinstance(value, list)
                collected += [value]
            else:
                assert isinstance(value, list)
                collected += value
        for subnode in next(node):
            _recursive_collect_impl_branch(node=subnode, next=next, collect=collect, flatten=flatten, visited=visited, collected=collected)
