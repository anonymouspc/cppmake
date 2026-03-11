#include <cppmake/error/config.hpp>
#include <cppmake/system/base.hpp>
#define BOOST_PROCESS_USE_STD_FS
#include <boost/process.hpp>

namespace cppmake
{
    class mach
        : public system
    {
        public:
            mach ( );
    };



    mach::mach ( )
    {
        #ifdef __MACH__
            this->system::executable_suffix = "";
            this->system::object_suffix     = "o";
            this->system::static_suffix     = "a";
            this->system::dynamic_suffix    = "dylib";
            this->system::compiler_path     = boost::process::environment::find_executable("clang++");
            this->system::install_dir       = "/usr";
        #else
            throw config_error("__MACH__ is not defined");
        #endif
    }
}