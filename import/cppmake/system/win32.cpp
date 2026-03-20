export module cppmake:system.win32;
import               :system.base;
import               :error.config;

namespace cppmake
{
    export class win32
      : public system_t
    {
        public:
            win32 ( );
    };



    win32::win32 ( )
    {
        #ifdef _WIN32
            this->name              = "win32"
            this->executable_suffix = "exe";
            this->object_suffix     = "obj";
            this->static_suffix     = "lib";
            this->dynamic_suffix    = "dll";
            this->compiler_path     = "cl.exe";
            this->linker_path       = "link.exe"
            this->install_dir       = "C:\\Program Files";
        #else
            throw config_error("_WIN32 is not defined");
        #endif
    }
}