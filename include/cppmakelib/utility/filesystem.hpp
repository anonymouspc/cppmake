#pragma once
#include <filesystem>
#define BOOST_PROCESS_USE_STD_FS
#include <boost/process.hpp>

namespace cppmake
{
    class absolute_path
        : public std::filesystem::path
    {

    };

    class relative_path
        : public std::filesystem::path
    {

    };

    class resolvable_path
        : public std::string
    {

    };

    std::filesystem::path resolve ( const resolvable_path& );



    std::filesystem::path resolve ( const resolvable_path& path )
    {
        return boost::process::environment::find_executable(static_cast<const std::string&>(path));
    }
}