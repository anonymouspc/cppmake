from cppmakelib.compiler.all       import compiler
from cppmakelib.error.logic        import LogicError
from cppmakelib.utility.decorator  import lifetime, member
from cppmakelib.utility.filesystem import add_file_suffix, join_path, parent_dir, path, try_create_dir
import atexit
import json
import re
import typing
if typing.TYPE_CHECKING:
    from cppmakelib.unit.code   import Code
    from cppmakelib.unit.module import Module
    from cppmakelib.unit.source import Source
    from cppmakelib.unit.object import Object


class UnitStatusLogger:
    # ========
    def           __init__                (self, build_cache_dir: path)                     -> None      : ...
    def           __del__                 (self)                                            -> None      : ...
    # ========
    def             get_code_preprocessed (self, code  : Code)                              -> bool      : ...
    def             set_code_preprocessed (self, code  : Code,    preprocessed: bool)       -> None      : ...
    # ========
    async def async_get_module_name       (self, module: Module)                            -> str       : ...
    def             set_module_name       (self, module: Module,  name        : str)        -> None      : ...
    async def async_get_module_imports    (self, module: Module)                            -> list[path]: ...
    async def async_set_module_imports    (self, module: Module,  imports     : list[path]) -> None      : ...
    def             get_module_precompiled(self, module: Module)                            -> bool      : ...
    def             set_module_precompiled(self, module: Module,  precompiled : bool)       -> None      : ...
    # ========
    async def async_get_source_imports    (self, source: Source)                            -> list[path]: ...
    async def async_set_source_imports    (self, source: Source,  imports     : list[path]) -> None      : ...
    def             get_source_compiled   (self, source: Source)                            -> bool      : ...
    def             set_source_compiled   (self, source: Source,  compiled    : bool)       -> None      : ...
    # ========
    def             get_object_shared     (self, object: Object)                            -> bool      : ...
    def             set_object_shared     (self, object: Object,  shared      : bool)       -> None      : ...
    def             get_object_linked     (self, object: Object)                            -> bool      : ...
    def             set_object_linked     (self, object: Object,  linked      : bool)       -> None      : ...
    # ========

    class _StatusNotFoundError(KeyError):
        pass
    def _get    (self, entry: list[str], check: dict[str, typing.Any], result: str)        -> typing.Any: ...
    def _set    (self, entry: list[str], check: dict[str, typing.Any], result: typing.Any) -> None      : ...
    def _reflect(self, variable: typing.Any, depth: int = 1)                               -> typing.Any: ...
    _file    : path  
    _content : typing.Any
    


@member(UnitStatusLogger)
def __init__(self: UnitStatusLogger, build_cache_dir: path) -> None:
    self._file = join_path(build_cache_dir, 'unit_status.json')
    try:
        self._content = json.load(open(self._file, 'r'))
    except:
        self._content = {}
    atexit.register(self.__del__)

@member(UnitStatusLogger)
@lifetime(open, json, print, create_dir, parent_dir)
def __del__(self: UnitStatusLogger) -> None:
    create_dir(parent_dir(self._file))
    json.dump(self._content, open(self._file, 'w'), indent=4)

@member(UnitStatusLogger)
def get_code_preprocessed(self: UnitStatusLogger, code: Code) -> bool:
    try:
        return self._get(entry=['code', 'preprocessed', code.file], check={'code': code, 'compiler': compiler}, result='preprocessed')
    except UnitStatusLogger._StatusNotFoundError:
        return False

@member(UnitStatusLogger)
def set_code_preprocessed(self: UnitStatusLogger, code: Code, preprocessed: bool) -> None:
    self._set(entry=['code', 'preprocessed', code.file], check={'code': code, 'compiler': compiler}, result={'preprocessed': preprocessed})

@member(UnitStatusLogger)
async def async_get_module_name(self: UnitStatusLogger, module: Module) -> str:
    try:
        name = self._get(entry=['module', 'name', module.file], check={'module': module, 'compiler': compiler}, result='name')
    except UnitStatusLogger._StatusNotFoundError:
        await module.async_preprocess()
        names = re.findall(
            pattern=r'^\s*(?:export\s+)?module\s+(\w+(?:[\.:]\w+)*)\s*;\s*$',
            string =open(module.preprocessed_file, 'r').read(),
            flags  =re.MULTILINE
        )
        if len(names) == 0:
            raise LogicError(f'module {module.file} does not have a export statement')
        elif len(names) == 1:
            name = names[0]
            self.set_module_name(module=module, name=name)
        elif len(names) >= 2:
            raise LogicError(f'module {module.file} has multiple export names (with names = {names})')
        else:
            assert False
    return name
        
@member(UnitStatusLogger)
def set_module_name(self: UnitStatusLogger, module: Module, name: str) -> None:
    self._set(entry=['module', 'name', module.file], check={'module': module, 'compiler': compiler}, result={'name': name})

@member(UnitStatusLogger)
async def async_get_module_imports(self: UnitStatusLogger, module: Module) -> list[path]:
    try:
        imports = self._get(entry=['module', 'imports', module.file], check={'module':  module, 'compiler': compiler}, result='imports')
    except UnitStatusLogger._StatusNotFoundError:
        await module.async_preprocess()
        imports = re.findall(
            pattern=r'^\s*(?:export\s+)?import\s+(\w+(?:[\.:]\w+)*)\s*;\s*$',
            string =open(module.preprocessed_file, 'r').read(),
            flags  =re.MULTILINE
        )
        imports = [join_path(module.context_package.import_dir, add_file_suffix(join_path(*re.split(pattern=r'[.:]', string=import_)), 'cpp')) for import_ in imports]
        await self.async_set_module_imports(module=module, imports=imports)
    return imports

@member(UnitStatusLogger)
async def async_set_module_imports(self: UnitStatusLogger, module: Module, imports: list[path]) -> None:
    self._set(entry=['module', 'imports', module.file], check={'module': module, 'compiler': compiler}, result={'imports': imports})

@member(UnitStatusLogger)
def get_module_precompiled(self: UnitStatusLogger, module: Module) -> bool:
    try:
        return self._get(entry=['module', 'precompiled', module.file], check={'module': module, 'compiler': compiler}, result='precompiled')
    except UnitStatusLogger._StatusNotFoundError:
        return False

@member(UnitStatusLogger)
def set_module_precompiled(self: UnitStatusLogger, module: Module, precompiled: bool) -> None:
    self._set(entry=['module', 'precompiled', module.file], check={'module': module, 'compiler': compiler}, result={'precompiled': precompiled})

@member(UnitStatusLogger)
async def async_get_source_imports(self: UnitStatusLogger, source: Source) -> list[path]:
    try:
        imports = self._get(entry=['source', 'imports', source.file], check={'source': source, 'compiler': compiler}, result='imports')
    except UnitStatusLogger._StatusNotFoundError:
        await source.async_preprocess()
        imports = re.findall(
            pattern=r'^\s*import\s+(\w+(?:[\.:]\w+)*)\s*;\s*$',
            string =open(source.preprocessed_file, 'r').read(),
            flags  =re.MULTILINE
        )
        imports = [join_path(source.context_package.import_dir, add_file_suffix(join_path(*re.split(pattern=r'[.:]', string=import_)), 'cpp')) for import_ in imports]
        await self.async_set_source_imports(source=source, imports=imports)
    return imports

@member(UnitStatusLogger)
async def async_set_source_imports(self: UnitStatusLogger, source: Source, imports: list[path]) -> None:
    self._set(entry=['source', 'imports', source.file], check={'source': source, 'compiler': compiler}, result={'imports': imports})

@member(UnitStatusLogger)
def get_source_compiled(self: UnitStatusLogger, source: Source) -> bool:
    try:
        return self._get(entry=['source', 'compiled', source.file], check={'source': source, 'compiler': compiler}, result='compiled')
    except UnitStatusLogger._StatusNotFoundError:
        return False

@member(UnitStatusLogger)
def set_source_compiled(self: UnitStatusLogger, source: Source, compiled: bool) -> None:
    self._set(entry=['source', 'compiled', source.file], check={'source': source, 'compiler': compiler}, result={'compiled': compiled})        

@member(UnitStatusLogger)
def get_object_libs(self: UnitStatusLogger, object: Object) -> list[path]:
    try:
        return self._get(entry=['object', 'libs', object.file], check={'object': object, 'compiler': compiler}, result='libs')
    except UnitStatusLogger._StatusNotFoundError:
        raise LogicError(f'object does not have a libs cache (from a module or source)')

@member(UnitStatusLogger)
def set_object_libs(self: UnitStatusLogger, object: Object, libs: list[path]) -> None:
    self._set(entry=['object', 'libs', object.file], check={'object': object, 'compiler': compiler}, result={'libs': libs})

@member(UnitStatusLogger)
def get_object_shared(self: UnitStatusLogger, object: Object) -> bool:
    try:
        return self._get(entry=['object', 'shared', object.file], check={'object': object, 'compiler': compiler}, result='shared')
    except UnitStatusLogger._StatusNotFoundError:
        return False
    
@member(UnitStatusLogger)
def set_object_shared(self: UnitStatusLogger, object: Object, shared: bool) -> None:
    self._set(entry=['object', 'shared', object.file], check={'object': object, 'compiler': compiler}, result={'shared': shared})

@member(UnitStatusLogger)
def get_object_linked(self: UnitStatusLogger, object: Object) -> bool:
    try:
        return self._get(entry=['object', 'linked', object.file], check={'object': object, 'compiler': compiler}, result='linked')
    except UnitStatusLogger._StatusNotFoundError:
        return False
    
@member(UnitStatusLogger)
def set_object_linked(self: UnitStatusLogger, object: Object, linked: bool) -> None:
    self._set(entry=['object', 'linked', object.file], check={'object': object, 'compiler': compiler}, result={'linked': linked})

@member(UnitStatusLogger)
def _get(self: UnitStatusLogger, entry: list[str], check: dict[str, typing.Any], result: str) -> typing.Any:
    ptr = self._content
    for subentry in entry:
        if subentry not in ptr.keys():
            raise UnitStatusLogger._StatusNotFoundError()
        ptr = ptr[subentry]
    for subcheck in check.keys():
        if ptr[subcheck] != self._reflect(check[subcheck]):
            raise UnitStatusLogger._StatusNotFoundError()
    return ptr[result]

@member(UnitStatusLogger)
def _set(self: UnitStatusLogger, entry: list[str], check: dict[str, typing.Any], result: typing.Any) -> None:
    ptr = self._content
    for subentry in entry:
        if subentry not in ptr.keys():
            ptr[subentry] = {}
        ptr = ptr[subentry]
    for subcheck in check.keys():
        ptr[subcheck] = self._reflect(check[subcheck])
    for subresult in result.keys():
        ptr[subresult] = self._reflect(result[subresult])

@member(UnitStatusLogger)
def _reflect(self: UnitStatusLogger, variable: typing.Any, depth: int = 1) -> typing.Any:
    if isinstance(variable, (bool, int, float, str)):
        return variable
    elif isinstance(variable, list):
        return [self._reflect(subvariable, depth - 1) for subvariable in typing.cast(list[typing.Any], variable) if self._reflect(subvariable, depth - 1) is not None]
    elif isinstance(variable, dict):
        return {subkey: self._reflect(subvalue, depth - 1) for subkey, subvalue in typing.cast(dict[typing.Any, typing.Any], variable).items() if self._reflect(subvalue, depth - 1) is not None}
    else:
        return {subkey: self._reflect(subvalue, depth - 1) for subkey, subvalue in vars(typing.cast(object, variable)).items() if not subkey.startswith('_') and self._reflect(subvalue, depth - 1) is not None} if depth >= 1 else None

        