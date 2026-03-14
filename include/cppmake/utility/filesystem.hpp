#pragma once
#include <filesystem>
#define BOOST_PROCESS_USE_STD_FS
#include <boost/process.hpp>

namespace cppmake
{
    using resolvable_path = std::string;
    std::filesystem::path resolve ( const resolvable_path& );



    std::filesystem::path resolvable ( const resolvable_path& path )
    {
        return boost::process::environment::find_executable(path);
    }
}