#pragma once
#include <filesystem>
#define BOOST_PROCESS_USE_STD_FS
#include <boost/process.hpp>

namespace cppmake
{
    using resolvable_path = std::string;

    void resolve ( resolvable_path );

    class resolvable_path
    {
        public:
            resolvable_path ( ) = default;
            resolvable_path ( std::string );

        public:
            std::filesystem::path resolve ( ) const;

        private:
            std::string path;
    };



    resolvable_path::resolvable_path ( std::string path )
        : path(path)
    {

    }

    std::filesystem::path resolvable_path::resolve ( ) const
    {
        return boost::process::environment::find_executable(this->path);
    }
}