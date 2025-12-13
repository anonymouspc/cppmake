from cppmakelib.basic.config          import config
from cppmakelib.error.config          import ConfigError
from cppmakelib.error.subprocess      import SubprocessError
from cppmakelib.execution.run         import async_run
from cppmakelib.file.file_system      import parent_path, exist_file, create_dir
from cppmakelib.logger.module_mapper  import module_mapper_logger
from cppmakelib.system.all            import system
from cppmakelib.utility.decorator     import member, once, syncable
from cppmakelib.utility.version       import parse_version
import re

class Gcc:
    name          = "gcc"
    module_suffix = ".gcm"
    object_suffix = ".o"
    def           __init__    (self, path="g++"):                                                                                                                                                                    ...
    async def     __ainit__   (self, path="g++"):                                                                                                                                                                    ...
    def             preprocess(self, file,                                                                               compile_flags=[],                define_macros={}):                                         ...
    async def async_preprocess(self, file,                                                                               compile_flags=[],                define_macros={}):                                         ...
    def             precompile(self, file, module_file, object_file,     module_dirs=[], include_dirs=[],                compile_flags=[],                define_macros={}, diagnose_file=None, optimize_file=None): ...
    async def async_precompile(self, file, module_file, object_file,     module_dirs=[], include_dirs=[],                compile_flags=[],                define_macros={}, diagnose_file=None, optimize_file=None): ...
    def             compile   (self, file, object_file, executable_file, module_dirs=[], include_dirs=[], link_files=[], compile_flags=[], link_flags=[], define_macros={}, diagnose_file=None, optimize_file=None): ...
    async def async_compile   (self, file, object_file, executable_file, module_dirs=[], include_dirs=[], link_files=[], compile_flags=[], link_flags=[], define_macros={}, diagnose_file=None, optimize_file=None): ...
    def             std_module(self):                                                                                                                                                                                ...
    async def async_std_module(self):                                                                                                                                                                                ...



@member(Gcc)
@syncable
async def __ainit__(self, path="g++"):
    self.path    = path
    self.version = await self._async_get_version()
    self.stdlib  = "libstdc++"
    self.compile_flags = [
        f"-std={config.std}", "-fmodules", 
         *(["-O0", "-g"] if config.type == "debug"   else
           ["-O3",     ] if config.type == "release" else
           ["-Os"      ] if config.type == "size"    else 
           []) 
    ]
    self.link_flags = [
        *([f"-fuse-ld={system.linker_path}"] if system.linker_path != "ld"                        else []),
        *(["-s"                            ] if config.type == "release" or config.type == "size" else []),
        "-lstdc++exp"
    ]
    self.define_macros = {
        **({"DEBUG"  : "true"} if config.type == "debug"   else
           {"DNDEBUG": "true"} if config.type == "release" else
           {})
    }

@member(Gcc)
@syncable
async def async_preprocess(self, file, compile_flags=[], define_macros={}):
    code = open(file, 'r').read()
    code = re.sub(r'^\s*#include(?!\s*<version>).*$', "", code, flags=re.MULTILINE)
    return await async_run(
        command=[
            self.path,
            *(self.compile_flags + compile_flags),
            *[f"-D{key}={value}" for key, value in (self.define_macros | define_macros).items()],
            "-E", "-x", "c++", "-",
            "-o", "-"
        ],
        input_stdin=code,
        print_stdout=False,
        return_stdout=True
    )

@member(Gcc)
@syncable
async def async_precompile(self, file, module_file, object_file, module_dirs=[], include_dirs=[], compile_flags=[], define_macros={}, diagnose_file=None, optimize_file=None):
    create_dir(parent_path(module_file))
    create_dir(parent_path(object_file))
    create_dir(parent_path(diagnose_file)) if diagnose_file is not None else None
    create_dir(parent_path(optimize_file)) if optimize_file is not None else None
    await async_run(
        command=[
            self.path,
            *(self.compile_flags + compile_flags),
            *[f"-fmodule-mapper={module_mapper_logger.get_mapper(module_dir)}" for module_dir  in module_dirs                                 ],
            *[f"-I{include_dir}"                                               for include_dir in include_dirs                                ],
            *[f"-D{key}={value}"                                               for key, value  in (self.define_macros | define_macros).items()],
            *([f"-fdiagnostics-add-output=sarif:file={diagnose_file}"] if diagnose_file is not None else []),
            *([f"-fopt-info-optimized={optimize_file}"]                if optimize_file is not None else []),
            "-c", file,
            "-o", object_file
        ],
        log_command=(True, file)
    )

@member(Gcc)
@syncable
async def async_compile(self, file, object_file, executable_file, module_dirs=[], include_dirs=[], link_files=[], compile_flags=[], link_flags=[], define_macros={}, diagnose_file=None, optimize_file=None):
    create_dir(parent_path(executable_file))
    create_dir(parent_path(diagnose_file)) if diagnose_file is not None else None
    create_dir(parent_path(optimize_file)) if optimize_file is not None else None
    await async_run(
        command=[
            self.path,
            *(self.compile_flags + compile_flags),
            *[f"-fmodule-mapper={module_mapper_logger.get_mapper(module_dir)}" for module_dir  in module_dirs                                 ],
            *[f"-I{include_dir}"                                               for include_dir in include_dirs                                ],
            *[f"-D{key}={value}"                                               for key, value  in (self.define_macros | define_macros).items()],
            *([f"-fdiagnostics-add-output=sarif:file={diagnose_file}"] if diagnose_file is not None else []),
            *([f"-fopt-info-optimized={optimize_file}"]                if optimize_file is not None else []),
            "-c", file,
            "-o", object_file
        ],
        log_command=(True, file)
    )
    await async_run(
        command=[
            self.path,
            *(self.link_flags + link_flags),
            *([object_file] + link_files),
            "-o", executable_file
        ]
    )

@member(Gcc)
@syncable
@once
async def async_std_module(self):
    verbose_info = await async_run(
        command=[self.path, "-v", "-E", "-x", "c++", "-"], 
        input_stdin="", 
        print_stderr=config.verbose, 
        return_stderr=True
    )
    search_dirs = re.search(r'^#include <...> search starts here:$\n(.*)\n^end of search list.$', verbose_info, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if search_dirs is None:
        raise ConfigError(f'libstdc++ module not found (with "{self.path} -v -E -x c++ -" outputs [[invalid message]])')
    search_dirs = [search_dir.strip() for search_dir in search_dirs.group(1).splitlines()]
    for include_dir in search_dirs:
        module_file = f"{include_dir}/bits/std.cc"
        if exist_file(module_file):
            return module_file
    else:
        raise ConfigError(f"libstdc++ module not found (with search_file = {', '.join([f"{include_dir}/bits/std.cc" for include_dir in search_dirs])})")
            
@member(Gcc)
async def _async_get_version(self):
    try:
        version_str = await async_run(command=[self.path, "--version"], return_stdout=True)
        if version_str.startswith("g++"):
            version = parse_version(version_str)
            if version >= 15:
                return version
            else:
                raise ConfigError(f'gcc is too old (with version = {version}, requires >= 15)')
        else:
            raise ConfigError(f'gcc is not valid (with "{self.path} --version" outputs "{version_str.replace('\n', ' ')}")')
    except SubprocessError as error:
        raise ConfigError(f'gcc is not valid (with "{self.path} --version" outputs "{error.stderr.replace('\n', ' ')}" and exits {error.code})')
    except FileNotFoundError as error:
        raise ConfigError(f'gcc is not found (with "{self.path} --version" fails "{error}")')