from cppmakelib.utility.decorator  import implement
from cppmakelib.utility.filesystem import path
import importlib.util
import types
import typing

def import_module(file: path, globals: dict[str, typing.Any] = {}) -> types.ModuleType | None: ...



@implement
def import_module(file: path, globals: dict[str, typing.Any] = {}) -> types.ModuleType | None:
    try:
        spec = importlib.util.spec_from_file_location(name=file, location=file)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        module.__dict__.update(globals)
        spec.loader.exec_module(module)
        return module
    except FileNotFoundError:
        return None


