export module cppmake:system.mach;
import               :system.base;
import               :error.config;

namespace cppmake
{
    export class mach
      : public system_t
    {
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