export module cppmake:system.linux;
import               :system.base;
import               :error.config;

namespace cppmake
{
    export class linux
      : public system_t
    {
        public:
            linux ( );
    };



    linux::linux ( )
    {
        #ifdef __linux__
            this->name              = "linux";
            this->executable_suffix = "";
            this->object_suffix     = "o";
            this->static_suffix     = "a";
            this->dynamic_suffix    = "so";
            this->compiler_path     = "g++";
            this->linker_path       = "ld";
            this->install_dir       = "/usr";
        #else
            throw config_error("__linux__ is not defined");
        #endif
    }
}