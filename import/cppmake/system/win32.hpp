#pragma once
#include <cppmakelib/error/config.hpp>
#include <cppmakelib/system/base.hpp>
#define BOOST_PROCESS_USE_STD_FS
#include <boost/process.hpp>

namespace cppmake
{
    class win32
      : public system_t
    {
        public:
            win32 ( );
    };



    win32::win32 ( )
    {
        #ifdef _WIN32
            this->system_t::name              = "win32"
            this->system_t::executable_suffix = "exe";
            this->system_t::object_suffix     = "obj";
            this->system_t::static_suffix     = "lib";
            this->system_t::dynamic_suffix    = "dll";
            this->system_t::compiler_path     = "cl.exe";
            this->system_t::linker_path       = "link.exe"
            this->system_t::install_dir       = "C:\\Program Files";
        #else
            throw config_error("_WIN32 is not defined");
        #endif
    }
}