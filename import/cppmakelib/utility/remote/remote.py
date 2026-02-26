from cppmakelib.compiler.all      import compiler
from cppmakelib.utility.filesystem import path
from cppmakelib.utility.decorator  import member

class RemoteCompiler:
    def __init__(self, protocol: Protocol): ...
    def preprocess(): ...
    def precompile(): ...
    def compile   (): ...
    def link      (): ...

class DistributedCompiler:
    def __init__(self, local_compiler: ..., remote_compilers: list[...]): ...
    def preprocess(): ...
    def precompile(): ...
    def compile   (): ...
    def link      (): ...

local_compiler   = compiler
remote_compilers = [RemoteCompiler(compiler) for compiler in config.remote_compilers]
compiler         = DistributeCompiler(local_compiler, remote_compilers)



@member(RemoteCompiler)
async def async_compile(
    self           : RemoteCompiler,
    source_file    : path,
    object_file    : path,
    compile_flags  : list[str]      = [],
    define_macros  : dict[str, str] = {}, 
    import_dirs    : list[path]     = [], 
    include_dirs   : list[path]     = []
) -> None:
    

@member(RemoteCompiler)
def precompile(
    self            : RemoteCompiler,
    module_file     : path,
    precompiled_file: path, 
    object_file     : path, 
    compiler_flags  : list[str],
    define_macros   : dict[str, str],
    include_dirs    : list[path],
    import_dirs     : list[path]
) -> None:
    await when_all(self.protocol.async_send_file(file) for file in recursive_collect(import_files...))
    await self.protocol.async_send_command(precompile, module_file, precompiled_file, object_file, ...)
    await self.protocol.async_receive_file(object_file)

