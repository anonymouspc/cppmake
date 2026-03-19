#pragma once
#include <cppmakelib/error/config.hpp>
#include <cppmakelib/system/base.hpp>
#define BOOST_PROCESS_USE_STD_FS
#include <boost/process.hpp>

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
            this->system_t::name              = "linux";
            this->system_t::executable_suffix = "";
            this->system_t::object_suffix     = "o";
            this->system_t::static_suffix     = "a";
            this->system_t::dynamic_suffix    = "so";
            this->system_t::compiler_path     = "g++";
            this->system_t::linker_path       = "ld";
            this->system_t::install_dir       = "/usr";
        #else
            throw config_error("__linux__ is not defined");
        #endif
    }
}