from cppmakelib.utility.decorator import implement
import os

env = dict[str, str]

def append_current_env(new_env: env) -> env : ...
def current_env       ()             -> env : ...
def set_current_env   (new_env: env) -> None: ...
def update_current_env(new_env: env) -> None: ...



@implement
def append_current_env(new_env: env) -> env:
    env = current_env()
    env.update(new_env)
    return env

@implement
def current_env() -> env:
    return os.environ.copy()

@implement
def set_current_env(new_env: env) -> None:
    os.environ = new_env

@implement
def update_current_env(new_env: env) -> None:
    os.environ.update(new_env)
