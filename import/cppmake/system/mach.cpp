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
            this->system_t::name              = "mach";
            this->system_t::executable_suffix = "";
            this->system_t::object_suffix     = "o";
            this->system_t::static_suffix     = "a";
            this->system_t::dynamic_suffix    = "dylib";
            this->system_t::compiler_path     = "clang++";
            this->system_t::linker_path       = "ld";
            this->system_t::install_dir       = "/usr";
        #else
            throw config_error("__MACH__ is not defined");
        #endif
    }
}