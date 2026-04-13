export module cppmake:system.mach;
import               :error.config;
import               :utility.filesystem;

namespace cppmake
{
    export class mach
    {
        public:
            static constexpr    std::string_view name              = "mach";
            static constexpr    std::string_view executable_suffix = "";
            static constexpr    std::string_view object_suffix     = ".o";
            static constexpr    std::string_view static_suffix     = ".a";
            static constexpr    std::string_view dynamic_suffix    = ".dylib";
            static const inline resolvable_path  compiler_path     = "clang++";
            static const inline resolvable_path  linker_path       = "ld";
            static const inline absolute_path    install_path      = "/usr";
            
        public:
            mach ( );
    };



    mach::mach ( )
    {
        #ifndef __MACH__
            throw config_error("__MACH__ is not defined");
        #endif
    }
}