from cppmakelib.basic.config       import config
from cppmakelib.logger.unit_status import UnitStatusLogger
from cppmakelib.utility.decorator  import member, once, unique
from cppmakelib.utility.filesystem import path
from cppmakelib.utility.import_    import import_module
import types
import typing

class Package:
    def __new__ (cls,  name: str) -> Package: ...
    def __init__(self, name: str) -> None   : ...
    def   build (self)            -> None   : ...
    # ========
    name               : str
    dir                : path
    # ========
    include_dir        : path # redefinable in cppmake.py
    import_dir         : path # redefinable in cppmake.py
    # ========
    build_dir          : path
    build_import_dir   : path
    build_include_dir  : path
    build_utility_dir  : path
    install_dir        : path
    install_bin_dir    : path
    install_import_dir : path
    install_include_dir: path
    install_lib_dir    : path
    # ========
    compile_flags      : list[str]      # redefinable in cppmake.py
    link_flags         : list[str]      # redefinable in cppmake.py
    define_macros      : dict[str, str] # redefinable in cppmake.py
    # ========
    require_packages   : list[Package]
    # ========
    unit_status_logger : UnitStatusLogger
    # ========
    cppmake_file       : path
    cppmake            : types.ModuleType | None
    # ========

class MainPackage(Package):
    def __new__ (cls)  -> typing.Self: ...
    def __init__(self) -> None       : ...
    def   build (self) -> None       : ...
    # ========
    name               : str  = 'main'
    dir                : path = '.'
    # ========
    include_dir        : path # redefinable in cppmake.py
    import_dir         : path # redefinable in cppmake.py
    # ========
    build_dir          : path
    build_import_dir   : path
    build_include_dir  : path
    build_utility_dir  : path
    install_dir        : path
    install_bin_dir    : path
    install_import_dir : path
    install_include_dir: path
    install_lib_dir    : path
    # ========
    compile_flags      : list[str]      # redefinable in cppmake.py
    link_flags         : list[str]      # redefinable in cppmake.py
    define_macros      : dict[str, str] # redefinable in cppmake.py
    # ========
    require_packages   : list[Package]
    # ========
    cppmake_file       : path
    cppmake            : types.ModuleType | None
    # ========



@member(Package)
@unique
def __init__(self: Package, name: str) -> None:
    self.name                = name
    self.dir                 = f'pkg/{self.name}'
    self.include_dir         = f'{self.dir}/include'
    self.import_dir          = f'{self.dir}/import'
    self.build_dir           = f'.cppmake/{config.type}/pkg/{self.name}/build'
    self.build_import_dir    = f'{self.build_dir}/import'
    self.build_include_dir   = f'{self.build_dir}/include'
    self.build_utility_dir   = f'{self.build_dir}/utility'
    self.install_dir         = f'.cppmake/{config.type}/pkg/{self.name}/install'
    self.install_bin_dir     = f'{self.install_dir}/bin'
    self.install_import_dir  = f'{self.install_dir}/import'
    self.install_include_dir = f'{self.install_dir}/include'
    self.install_lib_dir     = f'{self.install_dir}/lib'
    self.compile_flags       = []
    self.link_flags          = []
    self.define_macros       = {}
    self.require_packages    = []
    self.unit_status_logger  = UnitStatusLogger(build_utility_dir=self.build_utility_dir)
    self.cppmake_file        = f'{self.dir}/cppmake.py'
    from cppmakelib.basic.context import context
    with context.switch(package=self):
        self.cppmake = import_module(file=self.cppmake_file, globals={'self': self})

@member(Package)
@once
def build(self: Package) -> None:
    [package.build() for package in self.require_packages]
    from cppmakelib.basic.context import context
    with context.switch(package=self):
        print(f'build package {self.name}')
        self.cppmake.build() if self.cppmake is not None and hasattr(self.cppmake, 'build') else None

@member(MainPackage)
def __new__(cls: type[MainPackage]) -> MainPackage:
    return typing.cast(MainPackage, super(MainPackage, cls).__new__(cls, 'main'))

@member(MainPackage)
def __init__(self: MainPackage) -> None:
    self.name               = 'main'
    self.dir                = '.'
    self.include_dir        = 'include'
    self.import_dir         = 'import'
    self.build_dir          = f'.cppmake/{config.type}'
    self.build_import_dir   = f'{self.build_dir}/import'
    self.build_include_dir  = f'{self.build_dir}/include'
    self.build_utility_dir  = f'{self.build_dir}/utility'
    self.compile_flags      = []
    self.link_flags         = []
    self.define_macros      = {}
    self.require_packages   = []
    self.unit_status_logger = UnitStatusLogger(build_utility_dir=self.build_utility_dir)
    self.cppmake_file       = 'cppmake.py'
    self.cppmake            = import_module(file=self.cppmake_file, globals={'self': self})
    
@member(MainPackage)
@once
def build(self: MainPackage) -> None:
    [package.build() for package in self.require_packages]
    self.cppmake.build() if self.cppmake is not None and hasattr(self.cppmake, 'build') else None

main_package = MainPackage()
