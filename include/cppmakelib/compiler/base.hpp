#include "cppmakelib/utility/filesystem.hpp"
#include <cppmakelib/utility/concept.hpp>
#include <filesystem>
#include <map>
#include <vector>

namespace cppmake
{
    class compiler_t
    {
        public:
            std::string                        name;
            std::string                        preprocessed_suffix;
            std::string                        preparsed_suffix;
            std::string                        precompiled_suffix;
            resolvable_path                    file;
            version_t                          version;
            std::vector<std::string>           compile_args;
            std::vector<std::string>           link_args;
            std::map<std::string, std::string> define_macros;
            std::string                        stdlib_name;
            std::filesystem::path              stdlib_module_file;
            std::filesystem::path              stdlib_static_file;
            std::filesystem::path              stdlib_dynamic_file;

        public:
                  void             preprocess ( this const auto& self, const std::filesystem::path& code_file,   std::filesystem::path preprocessed_file,                                   iterable_as<std::string> auto compile_options, mappable_as<std::string, std::string> auto define_macros, iterable_as<std::filesystem::path> auto include_directories);
            async<void> auto async_preprocess ( this const auto& self, std::filesystem::path code_file,   std::filesystem::path preprocessed_file,                                   iterable_as<std::string> auto compile_options, mappable_as<std::string, std::string> auto define_macros, iterable_as<std::filesystem::path> auto include_directories);
                  void             prescan    ( this const auto& self, std::filesystem::path code_file,   std::filesystem::path prescanned_file,                                     iterable_as<std::string> auto compile_options, mappable_as<std::string, std::string> auto define_macros, iterable_as<std::filesystem::path> auto include_directories);
            async<void> auto async_prescan    ( this const auto& self, std::filesystem::path code_file,   std::filesystem::path prescanned_file,                                     iterable_as<std::string> auto compile_options, mappable_as<std::string, std::string> auto define_macros, iterable_as<std::filesystem::path> auto include_directories);
                  void             preparse   ( this const auto& self, std::filesystem::path header_file, std::filesystem::path preparsed_file,                                      iterable_as<std::string> auto compile_options, mappable_as<std::string, std::string> auto define_macros, iterable_as<std::filesystem::path> auto include_directories);
            async<void> auto async_preparse   ( this const auto& self, std::filesystem::path header_file, std::filesystem::path preparsed_file,                                      iterable_as<std::string> auto compile_options, mappable_as<std::string, std::string> auto define_macros, iterable_as<std::filesystem::path> auto include_directories);
                  void             precompile ( this const auto& self, std::filesystem::path module_file, std::filesystem::path precompiled_file, std::filesystem::path object_file, iterable_as<std::string> auto compile_options, mappable_as<std::string, std::string> auto define_macros, iterable_as<std::filesystem::path> auto import_directories, iterable_as<std::filesystem::path> auto include_directories);
            async<void> auto async_precompile ( this const auto& self, std::filesystem::path module_file, std::filesystem::path precompiled_file, std::filesystem::path object_file, iterable_as<std::string> auto compile_options, mappable_as<std::string, std::string> auto define_macros, iterable_as<std::filesystem::path> auto import_directories, iterable_as<std::filesystem::path> auto include_directories);
                  void             compile    ( this const auto& self, std::filesystem::path source_file, std::filesystem::path object_file,                                         iterable_as<std::string> auto compile_options, mappable_as<std::string, std::string> auto define_macros, iterable_as<std::filesystem::path> auto import_directories, iterable_as<std::filesystem::path> auto include_directories);
            async<void> auto async_compile    ( this const auto& self, std::filesystem::path source_file, std::filesystem::path object_file,                                         iterable_as<std::string> auto compile_options, mappable_as<std::string, std::string> auto define_macros, iterable_as<std::filesystem::path> auto import_directories, iterable_as<std::filesystem::path> auto include_directories);
            
    };
}