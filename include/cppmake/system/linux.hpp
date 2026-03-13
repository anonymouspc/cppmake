#pragma once
#define BOOST_PROCESS_USE_STD_FS
#include <boost/process.hpp>
#include <cppmake/error/config.hpp>
#include <cppmake/system/base.hpp>

namespace cppmake
{
    class linux
        : public system_t
    {
        public:
            linux ( );
    };



    linux::linux ( )
    {
        #ifdef __linux__
            this->system_t::executable_suffix = "";
            this->system_t::object_suffix     = "o";
            this->system_t::static_suffix     = "a";
            this->system_t::dynamic_suffix    = "so";
            this->system_t::compiler_path     = boost::process::environment::find_executable("g++");
            this->system_t::install_dir       = "/usr";
        #else
            throw config_error("__linux__ is not defined");
        #endif
    }
}