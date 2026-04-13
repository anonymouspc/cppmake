export module cppmake:system.mach;
import               :system.base;
import               :error.config;

namespace cppmake
{
    export class mach
    {
        public:
            static constexpr std::string_view name              = "linux";
            static constexpr std::string_view executable_suffix = "";
            static constexpr std::string_view object_suffix     = ".o";
            static constexpr std::string_view static_suffix     = ".a";
            static constexpr std::string_view dynamic_suffix    = ".so";
            static inline    resolvable_path  compiler_path     = "g++";
            static inline    resolvable_path  linker_path       = "ld";
            static inline    absolute_path    install_path      = "/usr";
            
        public:
            mach ( );
    };



    mach::mach ( )
    {
        #ifdef __MACH__
            this->name              = "mach";
            this->executable_suffix = "";
            this->object_suffix     = "o";
            this->static_suffix     = "a";
            this->dynamic_suffix    = "dylib";
            this->compiler_path     = "clang++";
            this->linker_path       = "ld";
            this->install_dir       = "/usr";
        #else
            throw config_error("__MACH__ is not defined");
        #endif
    }
}