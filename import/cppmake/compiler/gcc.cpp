export module cppmake:compiler.gcc;
import        std;

namespace cppmake
{
    class gcc
      : public compiler_t
    {
        public:
            gcc ( resolvable_path file );

        public:
                  void             preprocess ( std::filesystem::path code_file, std::filesystem::path preprocessed_file, iterable_as<std::string> auto compile_flags, mappable_as<std::string, std::string> auto define_macros, iterable_as<std::filesystem::path> auto include_directories);
            async<void> auto async_preprocess ( std::filesystem::path code_file, std::filesystem::path preprocessed_file, iterable_as<std::string> auto compile_flags, mappable_as<std::string, std::string> auto define_macros, iterable_as<std::filesystem::path> auto include_directories);
                  void             prescan    ( std::filesystem::path code_file, std::filesystem::path prescanned_file,   iterable_as<std::string> auto compile_flags, mappable_as<std::string, std::string> auto define_macros, iterable_as<std::filesystem::path> auto include_directories);
            async<void> auto async_prescan    ( std::filesystem::path code_file, std::filesystem::path prescanned_file,   iterable_as<std::string> auto compile_flags, mappable_as<std::string, std::string> auto define_macros, iterable_as<std::filesystem::path> auto include_directories);
                  void             prescan    ( std::filesystem::path code_file, std::filesystem::path prescanned_file,   iterable_as<std::string> auto compile_flags, mappable_as<std::string, std::string> auto define_macros, iterable_as<std::filesystem::path> auto include_directories);
            async<void> auto async_prescan    ( std::filesystem::path code_file, std::filesystem::path prescanned_file,   iterable_as<std::string> auto compile_flags, mappable_as<std::string, std::string> auto define_macros, iterable_as<std::filesystem::path> auto include_directories);

    };



}