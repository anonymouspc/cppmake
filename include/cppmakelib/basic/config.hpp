#pragma once
#include <cppmakelib/system/all.hpp>
#include <cppmakelib/utility/argv.hpp>
#include <cppmakelib/utility/filesystem.hpp>
#include <filesystem>
#include <istream>
#include <string>
#include <boost/asio.hpp>
#include <boost/program_options.hpp>

namespace cppmake
{
    struct __config_t;
    extern __config_t config;



    class __config_t
    {
        public:
            enum class compile_std_t  { cpp20, cpp23, cpp26 };
            enum class compile_type_t { debug, release, size };
            enum class link_type_t    { static_, dynamic, shared = dynamic };

        public:
            std::filesystem::path project_dir;
            std::filesystem::path build_dir;
            std::filesystem::path install_dir;
            resolvable_path       compiler_path;
            compile_std_t         compile_std;
            compile_type_t        compile_type;
            resolvable_path       linker_path;
            link_type_t           link_type;
            std::string           target;
            unsigned              jobs;
            bool                  verbose;
            bool                  dry;

        public:
            __config_t ( int argc, char** argv );

        public:
            friend std::istream& operator >> ( std::istream&, compile_std_t& );
            friend std::istream& operator >> ( std::istream&, compile_type_t& );
            friend std::istream& operator >> ( std::istream&, link_type_t& );
    };

    __config_t::__config_t ( int argc, char** argv )
    {
        auto option_description = boost::program_options::options_description("options");
        option_description.add_options()
            ("--project-dir",   boost::program_options::value<std::filesystem::path>     (&this->project_dir)  ->default_value("."))
            ("--build-dir",     boost::program_options::value<std::filesystem::path>     (&this->build_dir)    ->default_value(".cppmake"))
            ("--install-dir",   boost::program_options::value<std::filesystem::path>     (&this->install_dir)  ->default_value(system.install_dir))
            ("--compiler-path", boost::program_options::value<resolvable_path>           (&this->compiler_path)->default_value(system.compiler_path))
            ("--compile-std",   boost::program_options::value<__config_t::compile_std_t> (&this->compile_std)  ->default_value(__config_t::compile_std_t::cpp26))
            ("--compile-type",  boost::program_options::value<__config_t::compile_type_t>(&this->compile_type) ->default_value(__config_t::compile_type_t::debug))
            ("--linker-path",   boost::program_options::value<resolvable_path>           (&this->linker_path)  ->default_value(system.linker_path))
            ("--linker-type",   boost::program_options::value<__config_t::link_type_t>   (&this->link_type)    ->default_value(__config_t::link_type_t::static_))
            ("--target",        boost::program_options::value<std::string>               (&this->target)       ->default_value("make"))
            ("--jobs",          boost::program_options::value<unsigned>                  (&this->jobs)         ->default_value(std::thread::hardware_concurrency()))
            ("--verbose",       boost::program_options::bool_switch                      (&this->verbose)      ->default_value(false))
            ("--dry",           boost::program_options::bool_switch                      (&this->dry)          ->default_value(false));

        boost::program_options::command_line_parser(argc, argv).options(option_description).run();
    }

    std::istream& operator >> ( std::istream& left, __config_t::compile_std_t& right )
    {
        std::string compile_std_string;
        left >> compile_std_string;
        right = (compile_std_string == "c++20") ? __config_t::compile_std_t::cpp20 :
    }

    __config_t config = __config_t(argc, argv);
}