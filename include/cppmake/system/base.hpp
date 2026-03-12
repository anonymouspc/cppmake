#pragma once
#include <filesystem>
#include <string>

namespace cppmake
{
    class system
    {
        public:
            std::string           executable_suffix;
            std::string           object_suffix;
            std::string           static_suffix;
            std::string           dynamic_suffix;
            std::filesystem::path compiler_path;
            std::filesystem::path install_dir;
    };
}