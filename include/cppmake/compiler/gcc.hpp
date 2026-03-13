#pragma once
#include <ranges>
#include <cppmake/utility/filesystem.hpp>

namespace cppmake
{
    class gcc
    {
        public:
            gcc ( resolvable_path file );

        public:
            void preprocess ( std::filesystem::path code_file, std::filesystem::path preprocessed_file, std::ranges::random_access_range auto compile_options, std::map<std::string,std::string> define_macros, std::vector<std::filesystem::path> include_directories)
    };



}