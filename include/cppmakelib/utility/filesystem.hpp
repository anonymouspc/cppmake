#pragma once
#include <cassert>
#include <filesystem>
#define BOOST_PROCESS_USE_STD_FS
#include <boost/process.hpp>

namespace cppmake
{
    class absolute_path
      : public std::filesystem::path
    {
        public:
            absolute_path ( )                       = default;
            absolute_path ( const char* );
            absolute_path ( std::filesystem::path );
    };

    class relative_path
      : public std::filesystem::path
    {
        public:
            relative_path ( )                       = default;
            relative_path ( const char* );
            relative_path ( std::filesystem::path );
    };

    class resolvable_path
      : public std::string
    {
        public:
            resolvable_path ( )             = default;
            resolvable_path ( const char* );
            resolvable_path ( std::string );

        public:
            friend std::istream& operator >> ( std::istream&, resolvable_path& );
    };

    std::filesystem::path resolve ( const resolvable_path& );



    absolute_path::absolute_path ( const char* path )
      : absolute_path(std::filesystem::path(path))
    {

    }

    absolute_path::absolute_path ( std::filesystem::path path )
      : std::filesystem::path(std::move(path))
    {
        assert(this->std::filesystem::path::is_absolute());
    }

    relative_path::relative_path ( const char* path )
      : relative_path(std::filesystem::path(path))
    {

    }

    relative_path::relative_path ( std::filesystem::path path )
      : std::filesystem::path(std::move(path))
    {
        assert(this->std::filesystem::path::is_relative());
    }

    resolvable_path::resolvable_path ( const char* path )
      : resolvable_path(std::filesystem::path(path))
    {

    }
    
    resolvable_path::resolvable_path ( std::string path )
      : std::string(std::move(path))
    {
        
    }

    std::filesystem::path resolve ( const resolvable_path& path )
    {
        return boost::process::environment::find_executable(static_cast<const std::string&>(path));
    }

    std::istream& operator >> ( std::istream& left, resolvable_path& right )
    {
        return left >> static_cast<std::string&>(right);
    }
}