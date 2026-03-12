#pragma once
#define BOOST_PROCESS_USE_STD_FS
#include <boost/process.hpp>
#include <cppmake/error/config.hpp>
#include <cppmake/system/base.hpp>

namespace cppmake
{
    class linux
        : public system
    {
        public:
            linux ( );
    };



    linux::linux ( )
    {
        #ifdef __linux__
            this->system::executable_suffix = "";
            this->system::object_suffix     = "o";
            this->system::static_suffix     = "a";
            this->system::dynamic_suffix    = "so";
            this->system::compiler_path     = boost::process::environment::find_executable("g++");
            this->system::install_dir       = "/usr";
        #else
            throw config_error("__linux__ is not defined");
        #endif
    }
}