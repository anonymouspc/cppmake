import typing

@typing.overload
def func(x: int) -> int: ...

@typing.overload
def func(x: float) -> float: ...

# print(func.__is_overload__)
print(func.__code__.

def func(x):
    return x

print(typing.get_overloads(func))
