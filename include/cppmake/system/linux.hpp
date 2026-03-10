#include <filesystem>
#include <string>
#define BOOST_PROCESS_USE_STD_FS
#include <boost/process.hpp>

namespace cppmake
{
    class linux
    {
        public:
            inline static std::string           executable_suffix = "";
            inline static std::string           object_suffix     = "o";
            inline static std::string           static_suffix     = "a";
            inline static std::string           dynamic_suffix    = "so";
            inline static std::filesystem::path compiler          = boost::process::environment::find_executable("g++");
            inline static std::filesystem::path install_dir       = "/usr";
    
        public:
            linux ( );
    };



    linux::linux ( )
    {
        #ifndef __linux__
            throw config_error("__linux__ is not defined");
        #endif
    }
}