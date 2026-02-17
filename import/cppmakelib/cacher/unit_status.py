from cppmakelib.compiler.all       import compiler
from cppmakelib.error.logic        import LogicError
from cppmakelib.utility.decorator  import lifetime, member
from cppmakelib.utility.filesystem import add_file_suffix, join_path, new_dir, parent_dir, path
import atexit
import json
import re
import typing
if typing.TYPE_CHECKING:
    from cppmakelib.unit.code   import Code
    from cppmakelib.unit.module import Module
    from cppmakelib.unit.source import Source
    from cppmakelib.unit.object import Object


class UnitStatusCacher:
    # ========
    def           __init__                (self: UnitStatusCacher, build_cache_dir: path)                     -> None      : ...
    def           __del__                 (self: UnitStatusCacher)                                            -> None      : ...
    # ========
    def             get_code_preprocessed (self: UnitStatusCacher, code  : Code)                              -> bool      : ...
    def             set_code_preprocessed (self: UnitStatusCacher, code  : Code,    preprocessed: bool)       -> None      : ...
    # ========
    async def async_get_module_name       (self: UnitStatusCacher, module: Module)                            -> str       : ...
    def             set_module_name       (self: UnitStatusCacher, module: Module,  name        : str)        -> None      : ...
    async def async_get_module_imports    (self: UnitStatusCacher, module: Module)                            -> list[str]: ...
    def             set_module_imports    (self: UnitStatusCacher, module: Module,  imports     : list[str])  -> None      : ...
    def             get_module_precompiled(self: UnitStatusCacher, module: Module)                            -> bool      : ...
    def             set_module_precompiled(self: UnitStatusCacher, module: Module,  precompiled : bool)       -> None      : ...
    # ========
    async def async_get_source_imports    (self: UnitStatusCacher, source: Source)                            -> list[str]: ...
    def             set_source_imports    (self: UnitStatusCacher, source: Source,  imports     : list[str])  -> None      : ...
    def             get_source_compiled   (self: UnitStatusCacher, source: Source)                            -> bool      : ...
    def             set_source_compiled   (self: UnitStatusCacher, source: Source,  compiled    : bool)       -> None      : ...
    # ========
    def             get_object_shared     (self: UnitStatusCacher, object: Object)                            -> bool      : ...
    def             set_object_shared     (self: UnitStatusCacher, object: Object,  shared      : bool)       -> None      : ...
    def             get_object_linked     (self: UnitStatusCacher, object: Object)                            -> bool      : ...
    def             set_object_linked     (self: UnitStatusCacher, object: Object,  linked      : bool)       -> None      : ...
    # ========

    class _StatusNeedsUpdateError(KeyError):
        pass
    def _get    (self: UnitStatusCacher, entry: list[str], check: dict[str, typing.Any], result: str)        -> typing.Any: ...
    def _set    (self: UnitStatusCacher, entry: list[str], check: dict[str, typing.Any], result: typing.Any) -> None      : ...
    def _reflect(self: UnitStatusCacher, variable: typing.Any, depth: int = 1)                               -> typing.Any: ...
    _file    : path  
    _content : typing.Any
    


@member(UnitStatusCacher)
def __init__(self: UnitStatusCacher, build_cache_dir: path) -> None:
    self._file = join_path(build_cache_dir, 'unit_status.json')
    try:
        self._content = json.load(open(self._file, 'r'))
    except:
        self._content = {}
    atexit.register(self.__del__)

@member(UnitStatusCacher)
@lifetime(open, json, print, new_dir, parent_dir)
def __del__(self: UnitStatusCacher) -> None:
    new_dir(parent_dir(self._file), exist_ok=True)
    json.dump(self._content, open(self._file, 'w'), indent=4)

@member(UnitStatusCacher)
def get_code_preprocessed(self: UnitStatusCacher, code: Code) -> bool:
    try:
        return self._get(entry=['code', 'preprocessed', code.file], check={'code': code, 'compiler': compiler}, result='preprocessed')
    except UnitStatusCacher._StatusNeedsUpdateError:
        return False

@member(UnitStatusCacher)
def set_code_preprocessed(self: UnitStatusCacher, code: Code, preprocessed: bool) -> None:
    self._set(entry=['code', 'preprocessed', code.file], check={'code': code, 'compiler': compiler}, result={'preprocessed': preprocessed})

@member(UnitStatusCacher)
async def async_get_module_name(self: UnitStatusCacher, module: Module) -> str:
    try:
        name = self._get(entry=['module', 'name', module.file], check={'module': module, 'compiler': compiler}, result='name')
    except UnitStatusCacher._StatusNeedsUpdateError:
        await module.async_preprocess()
        names = re.findall(
            pattern=r'^\s*(?:export\s+)?module\s+(\w+(?:[\.:]\w+)*)\s*;\s*$',
            string =open(module.preprocessed_file, 'r').read(),
            flags  =re.MULTILINE
        )
        if len(names) == 0:
            raise LogicError(f'module {module.file} does not have an export name')
        elif len(names) == 1:
            name = names[0]
            self.set_module_name(module=module, name=name)
        elif len(names) >= 2:
            raise LogicError(f'module {module.file} has multiple export names (with names = {names})')
        else:
            assert False
    return name
        
@member(UnitStatusCacher)
def set_module_name(self: UnitStatusCacher, module: Module, name: str) -> None:
    self._set(entry=['module', 'name', module.file], check={'module': module, 'compiler': compiler}, result={'name': name})

@member(UnitStatusCacher)
async def async_get_module_imports(self: UnitStatusCacher, module: Module) -> list[path]:
    try:
        imports = self._get(entry=['module', 'imports', module.file], check={'module':  module, 'compiler': compiler}, result='imports')
    except UnitStatusCacher._StatusNeedsUpdateError:
        await module.async_preprocess()
        imports = re.findall(
            pattern=r'^\s*(?:export\s+)?import\s+(\w+(?:[\.:]\w+)*)\s*;\s*$',
            string =open(module.preprocessed_file, 'r').read(),
            flags  =re.MULTILINE
        )
        imports = [join_path(module.context_package.import_dir, add_file_suffix(join_path(*re.split(pattern=r'[.:]', string=import_)), 'cpp')) for import_ in imports]
        self.set_module_imports(module=module, imports=imports)
    return imports

@member(UnitStatusCacher)
def set_module_imports(self: UnitStatusCacher, module: Module, imports: list[path]) -> None:
    self._set(entry=['module', 'imports', module.file], check={'module': module, 'compiler': compiler}, result={'imports': imports})

@member(UnitStatusCacher)
def get_module_precompiled(self: UnitStatusCacher, module: Module) -> bool:
    try:
        return self._get(entry=['module', 'precompiled', module.file], check={'module': module, 'compiler': compiler}, result='precompiled')
    except UnitStatusCacher._StatusNeedsUpdateError:
        return False

@member(UnitStatusCacher)
def set_module_precompiled(self: UnitStatusCacher, module: Module, precompiled: bool) -> None:
    self._set(entry=['module', 'precompiled', module.file], check={'module': module, 'compiler': compiler}, result={'precompiled': precompiled})

@member(UnitStatusCacher)
async def async_get_source_imports(self: UnitStatusCacher, source: Source) -> list[path]:
    try:
        imports = self._get(entry=['source', 'imports', source.file], check={'source': source, 'compiler': compiler}, result='imports')
    except UnitStatusCacher._StatusNeedsUpdateError:
        await source.async_preprocess()
        imports = re.findall(
            pattern=r'^\s*import\s+(\w+(?:[\.:]\w+)*)\s*;\s*$',
            string =open(source.preprocessed_file, 'r').read(),
            flags  =re.MULTILINE
        )
        imports = [join_path(source.context_package.import_dir, add_file_suffix(join_path(*re.split(pattern=r'[.:]', string=import_)), 'cpp')) for import_ in imports]
        self.set_source_imports(source=source, imports=imports)
    return imports

@member(UnitStatusCacher)
def set_source_imports(self: UnitStatusCacher, source: Source, imports: list[path]) -> None:
    self._set(entry=['source', 'imports', source.file], check={'source': source, 'compiler': compiler}, result={'imports': imports})

@member(UnitStatusCacher)
def get_source_compiled(self: UnitStatusCacher, source: Source) -> bool:
    try:
        return self._get(entry=['source', 'compiled', source.file], check={'source': source, 'compiler': compiler}, result='compiled')
    except UnitStatusCacher._StatusNeedsUpdateError:
        return False

@member(UnitStatusCacher)
def set_source_compiled(self: UnitStatusCacher, source: Source, compiled: bool) -> None:
    self._set(entry=['source', 'compiled', source.file], check={'source': source, 'compiler': compiler}, result={'compiled': compiled})        

@member(UnitStatusCacher)
def get_object_shared(self: UnitStatusCacher, object: Object) -> bool:
    try:
        return self._get(entry=['object', 'shared', object.file], check={'object': object, 'compiler': compiler}, result='shared')
    except UnitStatusCacher._StatusNeedsUpdateError:
        return False
    
@member(UnitStatusCacher)
def set_object_shared(self: UnitStatusCacher, object: Object, shared: bool) -> None:
    self._set(entry=['object', 'shared', object.file], check={'object': object, 'compiler': compiler}, result={'shared': shared})

@member(UnitStatusCacher)
def get_object_linked(self: UnitStatusCacher, object: Object) -> bool:
    try:
        return self._get(entry=['object', 'linked', object.file], check={'object': object, 'compiler': compiler}, result='linked')
    except UnitStatusCacher._StatusNeedsUpdateError:
        return False
    
@member(UnitStatusCacher)
def set_object_linked(self: UnitStatusCacher, object: Object, linked: bool) -> None:
    self._set(entry=['object', 'linked', object.file], check={'object': object, 'compiler': compiler}, result={'linked': linked})

@member(UnitStatusCacher)
def _get(self: UnitStatusCacher, entry: list[str], check: dict[str, typing.Any], result: str) -> typing.Any:
    ptr = self._content
    for subentry in entry:
        if subentry not in ptr.keys():
            raise UnitStatusCacher._StatusNeedsUpdateError()
        ptr = ptr[subentry]
    for subcheck in check.keys():
        if ptr[subcheck] != self._reflect(check[subcheck]):
            raise UnitStatusCacher._StatusNeedsUpdateError()
    return ptr[result]

@member(UnitStatusCacher)
def _set(self: UnitStatusCacher, entry: list[str], check: dict[str, typing.Any], result: typing.Any) -> None:
    ptr = self._content
    for subentry in entry:
        if subentry not in ptr.keys():
            ptr[subentry] = {}
        ptr = ptr[subentry]
    for subcheck in check.keys():
        ptr[subcheck] = self._reflect(check[subcheck])
    for subresult in result.keys():
        ptr[subresult] = self._reflect(result[subresult])

@member(UnitStatusCacher)
def _reflect(self: UnitStatusCacher, variable: typing.Any, depth: int = 2) -> typing.Any:
    if isinstance(variable, (bool, int, float, str)):
        return variable
    elif isinstance(variable, list):
        return [self._reflect(subvariable, depth - 1) for subvariable in typing.cast(list[typing.Any], variable) if self._reflect(subvariable, depth - 1) is not None]
    elif isinstance(variable, dict):
        return {subkey: self._reflect(subvalue, depth - 1) for subkey, subvalue in typing.cast(dict[typing.Any, typing.Any], variable).items() if self._reflect(subvalue, depth - 1) is not None}
    else:
        return {subkey: self._reflect(subvalue, depth - 1) for subkey, subvalue in vars(typing.cast(object, variable)).items() if not subkey.startswith('_') and self._reflect(subvalue, depth - 1) is not None} if depth >= 1 else None

        