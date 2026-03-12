#pragma once
#define BOOST_PROCESS_USE_STD_FS
#include <boost/process.hpp>
#include <cppmake/error/config.hpp>
#include <cppmake/system/base.hpp>

namespace cppmake
{
    class win32
        : public system
    {
        public:
            win32 ( );
    };



    win32::win32 ( )
    {
        #ifdef _WIN32
            this->system::executable_suffix = "exe";
            this->system::object_suffix     = "obj";
            this->system::static_suffix     = "lib";
            this->system::dynamic_suffix    = "dll";
            this->system::compiler_path     = boost::process::environment::find_executable("cl.exe");
            this->system::install_dir       = "C:\\Program Files";
        #else
            throw config_error("_WIN32 is not defined");
        #endif
    }
}