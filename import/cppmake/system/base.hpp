#pragma once
#include <cppmakelib/utility/filesystem.hpp>
#include <filesystem>
#include <string>

namespace cppmake
{
    class system_t
    {
        public:
            std::string           name;
            std::string           executable_suffix;
            std::string           object_suffix;
            std::string           static_suffix;
            std::string           dynamic_suffix;
            resolvable_path       compiler_path;
            resolvable_path       linker_path;
            std::filesystem::path install_dir;
    };
}