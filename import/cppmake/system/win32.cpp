export module cppmake:system.win32;
import               :error.config;
import               :utility.filesystem;

namespace cppmake
{
    export class win32
    {
        public:
            static constexpr    std::string_view name              = "win32";
            static constexpr    std::string_view executable_suffix = "exe";
            static constexpr    std::string_view object_suffix     = ".obj";
            static constexpr    std::string_view static_suffix     = ".lib";
            static constexpr    std::string_view dynamic_suffix    = ".dll";
            static const inline resolvable_path  compiler_path     = "cl.exe";
            static const inline resolvable_path  linker_path       = "link.exe";
            static const inline absolute_path    install_path      = "C:\\Program Files";

        public:
            win32 ( );
    };



    win32::win32 ( )
    {
        #ifndef _WIN32
            throw config_error("_WIN32 is not defined");
        #endif
    }
}