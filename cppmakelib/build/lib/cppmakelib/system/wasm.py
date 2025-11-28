from cppmakelib.system.all import system

class Wasm:
    name              = "wasm"
    executable_suffix = ".js"
    static_suffix     = system.static_suffix
    shared_suffix     = system.shared_suffix
    compiler_path     = "em++"
    linker_path       = system.linker_path
