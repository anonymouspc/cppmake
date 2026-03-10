#include <filesystem>
#include <string>
#define BOOST_PROCESS_USE_STD_FS
#include <boost/process.hpp>

namespace cppmake
{
    class win32
    {
        public:
            inline static std::string           executable_suffix = "exe";
            inline static std::string           object_suffix     = "obj";
            inline static std::string           static_suffix     = "lib";
            inline static std::string           dynamic_suffix    = "dll";
            inline static std::filesystem::path compiler          = boost::process::environment::find_executable("cl.exe");
            inline static std::filesystem::path install_dir       = "C:\\Program Files";
    
        public:
            win32 ( );
    };



    win32::win32 ( )
    {
        #ifndef _WIN32 
            throw config_error("_WIN32 is not defined");
        #endif
    }
}