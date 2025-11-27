from cppmakelib.basic.config   import config
from cppmakelib.compiler.clang import Clang
from cppmakelib.compiler.gcc   import Gcc
from cppmakelib.compiler.msvc  import Msvc
from cppmakelib.error.config   import ConfigError

compiler = ...



suberrors = []
for Compiler in (Clang, Gcc, Msvc):
    try:
        compiler = Compiler(config.compiler)
        break
    except ConfigError as error:
        suberrors += [error]
else:
    raise ConfigError(f'compiler "{config.compiler}" is not supported, because\n{'\n'.join([f"  {error}" for error in suberrors])}')

