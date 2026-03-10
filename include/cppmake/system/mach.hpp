#include <filesystem>
#include <string>
#define BOOST_PROCESS_USE_STD_FS
#include <boost/process.hpp>

namespace cppmake
{
    class mach
    {
        public:
            inline static std::string           executable_suffix = "";
            inline static std::string           object_suffix     = "o";
            inline static std::string           static_suffix     = "a";
            inline static std::string           dynamic_suffix    = "dylib";
            inline static std::filesystem::path compiler          = boost::process::environment::find_executable("clang++");
            inline static std::filesystem::path install_dir       = "/usr";
    
        public:
            mach ( );
    };



    mach::mach ( )
    {
        #ifndef __MACH__
            throw config_error("__MACH__ is not defined");
        #endif
    }
}