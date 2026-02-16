from cppmakelib.basic.config       import config
from cppmakelib.logger.unit_status import UnitStatusLogger
from cppmakelib.utility.decorator  import member, once
from cppmakelib.utility.filesystem import current_dir, join_path, path
from cppmakelib.utility.import_    import import_module
import types
import typing
if typing.TYPE_CHECKING:
    from cppmakelib.package.basic import Package

class MainPackage(Package):
    def           __new__  (cls)  -> MainPackage: ...
    def           __init__ (self) -> None       : ...
    def             build  (self) -> None       : ...
    async def async_build  (self) -> None       : ...
    def             install(self) -> None       : ...
    async def async_install(self) -> None       : ...
    # ========
    name               : str  = 'main'
    dir                : path = ''
    # ========
    include_dir        : path # redefinable in cppmake.py
    import_dir         : path # redefinable in cppmake.py
    pkg_dir            : path # redefinable in cppmake.py
    # ========
    build_dir          : path
    build_import_dir   : path
    build_include_dir  : path
    build_cache_dir    : path
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
    unit_status_cacher : UnitStatusLogger
    # ========
    cppmake_file       : path
    cppmake            : types.ModuleType | None
    # ========

@member(MainPackage)
def __init__(self: MainPackage) -> None:
    self.name                = 'main'
    self.dir                 = current_dir()
    self.include_dir         = 'include'
    self.import_dir          = 'import'
    self.pkg_dir             = 'pkg'
    self.build_dir           = join_path(config.build_dir, config.type)
    self.build_import_dir    = join_path(self.build_dir, 'import')
    self.build_include_dir   = join_path(self.build_dir, 'include')
    self.build_cache_dir     = join_path(self.build_dir, '.cache')
    self.install_dir         = config.install_dir
    self.install_bin_dir     = join_path(self.install_dir, 'bin')
    self.install_import_dir  = join_path(self.install_dir, 'import')
    self.install_include_dir = join_path(self.install_dir, 'include')
    self.install_lib_dir     = join_path(self.install_dir, 'lib')
    self.compile_flags       = []
    self.link_flags          = []
    self.define_macros       = {}
    self.require_packages    = []
    self.unit_status_cacher  = UnitStatusLogger(build_cache_dir=self.build_cache_dir)
    self.cppmake_file        = 'cppmake.py'
    self.cppmake             = import_module(file=self.cppmake_file, globals={'self': self})
    
@member(MainPackage)
@once
def build(self: MainPackage) -> None:
    [package.install() for package in self.require_packages]
    self.cppmake.build() if self.cppmake is not None and hasattr(self.cppmake, 'build') else None

@member(MainPackage)
@once
async def async_install(self: MainPackage) -> None:
    self.cppmake.install() if self.cppmake is not None and hasattr(self.cppmake, 'install') else None

main_package = MainPackage()