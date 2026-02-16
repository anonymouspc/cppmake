from cppmakelib.basic.config       import config
from cppmakelib.basic.context      import context
from cppmakelib.compiler.all       import compiler
from cppmakelib.executor.scheduler import scheduler
from cppmakelib.package.basic      import Package
from cppmakelib.unit.preprocessed  import Preprocessed
from cppmakelib.utility.algorithm  import recursive_collect
from cppmakelib.utility.decorator  import member, once, pre, syncable, unique_in
from cppmakelib.utility.filesystem import get_file_modify_time, join_path, normal_path, path, relative_path, replace_file_suffix
from cppmakelib.utility.time       import time

class Code:
    def           __new__          (cls : type[Code], file: path) -> Code        : ...
    def           __init__         (self: Code,       file: path) -> None        : ...
    async def    __ainit__         (self: Code,       file: path) -> None        : ...
    def             preprocess     (self: Code)                   -> Preprocessed: ...
    async def async_preprocess     (self: Code)                   -> Preprocessed: ...
    def             is_preprocessed(self: Code)                   -> bool        : ...
    async def async_is_preprocessed(self: Code)                   -> bool        : ...
    file             : path
    modify_time      : time
    context_package  : Package
    preprocessed_file: path
    compile_flags    : list[str]
    define_macros    : dict[str, str]



@member(Code)
@syncable
@unique_in(context.package)
@pre(1, normal_path)
async def __ainit__(self: Code, file: path) -> None:
    self.file              = file
    self.modify_time       = get_file_modify_time(self.file)
    self.context_package   = context.package
    self.preprocessed_file = join_path(self.context_package.build_dir, replace_file_suffix(relative_path(from_path=self.context_package.dir, to_path=self.file), compiler.preprocessed_suffix))
    self.compile_flags     = self.context_package.compile_flags
    self.define_macros     = self.context_package.define_macros

@member(Code)
@syncable
@once
async def async_preprocess(self: Code) -> Preprocessed:
    if not await self.async_is_preprocessed():
        async with scheduler.schedule():
            print(f'preprocess code {self.file}') if config.verbose else None
            await compiler.async_preprocess(
                code_file        =self.file,
                preprocessed_file=self.preprocessed_file,
                compile_flags    =self.compile_flags,
                define_macros    =self.define_macros,
                include_dirs     =[self.context_package.include_dir] + recursive_collect(self.context_package, next=lambda package: package.require_packages, collect=lambda package: package.install_include_dir)
            )
        self.context_package.unit_status_cacher.set_code_preprocessed(code=self, preprocessed=True)
    return Preprocessed(self.preprocessed_file)

@member(Code)
@syncable
@once
async def async_is_preprocessed(self: Code) -> bool:
    return self.context_package.unit_status_cacher.get_code_preprocessed(code=self)
               