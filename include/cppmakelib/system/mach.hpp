#pragma once
#define BOOST_PROCESS_USE_STD_FS
#include <boost/process.hpp>
#include <cppmakelib/error/config.hpp>
#include <cppmakelib/system/base.hpp>

namespace cppmake
{
    class mach
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
            this->system_t::compiler_path     = boost::process::environment::find_executable("clang++");
            this->system_t::install_dir       = "/usr";
        #else
            throw config_error("__MACH__ is not defined");
        #endif
    }
}