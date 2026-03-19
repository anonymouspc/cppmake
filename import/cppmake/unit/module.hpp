#pragma once
#include <cppmakelib/unit/header.hpp>
#include <chrono>
#include <filesystem>
#include <map>
#include <string>
#include <vector>

namespace cppmake
{
    class module
    {
        public:
            std::filesystem::path              file;
            std::filesystem::path              precompiled_file;
            std::filesystem::path              object_file;
            std::string                        name;
            std::chrono::file_clock            modify_time;
            std::vector<std::string>           compile_args;
            std::map<std::string, std::string> define_macros;
            std::vector<module>                import_modules;
            std::vector<header>                include_headers;

        public:
            

        public:
                  precompiled       precompile     ( );
            async<precompiled> auto precompile     ( );
                  bool              is_precompiled ( );
            async<bool>        auto is_precompiled ( );
    };
}