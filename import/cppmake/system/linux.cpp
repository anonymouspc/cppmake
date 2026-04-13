export module cppmake:system.linux;
import               :error.config;
import               :utility.filesystem;

namespace cppmake
{
    export class linux
    {
        public:
            static constexpr    std::string_view name              = "linux";
            static constexpr    std::string_view executable_suffix = "";
            static constexpr    std::string_view object_suffix     = ".o";
            static constexpr    std::string_view static_suffix     = ".a";
            static constexpr    std::string_view dynamic_suffix    = ".so";
            static const inline resolvable_path  compiler_path     = "g++";
            static const inline resolvable_path  linker_path       = "ld";
            static const inline absolute_path    install_path      = "/usr";

        public:
            linux ( );
    };



    linux::linux ( )
    {
        #ifndef __linux__
            throw config_error("__linux__ is not defined");
        #endif
    }
}