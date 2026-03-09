import sys
sys.dont_write_bytecode = True

from cppmakelib.basic.config        import config

from cppmakelib.compiler.all        import compiler
from cppmakelib.compiler.clang      import Clang
from cppmakelib.compiler.emcc       import Emcc
from cppmakelib.compiler.gcc        import Gcc

from cppmakelib.error.config        import ConfigError
from cppmakelib.error.logic         import LogicError
from cppmakelib.error.subprocess    import SubprocessError

from cppmakelib.executor.operation  import sync_wait, start_detached, when_all, when_any
from cppmakelib.executor.run        import async_run

from cppmakelib.package.basic       import Package
from cppmakelib.package.main        import main_package

from cppmakelib.system.all          import system
from cppmakelib.system.linux        import Linux
from cppmakelib.system.macos        import Macos
from cppmakelib.system.windows      import Windows

from cppmakelib.unit.executable     import Executable
from cppmakelib.unit.module         import Module
from cppmakelib.unit.source         import Source

from cppmakelib.utility.filesystem  import copy_file, copy_dir, iterate_dir, recursive_iterate_dir

self: Package
