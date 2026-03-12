#pragma once
#include <filesystem>
#include <string>
#include <boost/asio.hpp>
#include <boost/program_options.hpp>
#include <cppmake/system/all.hpp>
#include <cppmake/utility/filesystem.hpp>

namespace cppmake
{
    struct config_t
    {
        enum class compile_std_t  { cpp20, cpp23, cpp26 };
        enum class compile_type_t { debug, release, size };
        enum class link_type_t    { static_, dynamic, shared = dynamic };

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

        config_t ( )                       = default;
        config_t ( int argc, char** argv );
    };

    config_t config = config_t();



    struct __system { resolvable_path compiler_path = std::string("g++"); resolvable_path linker_path = std::string("ld"); std::filesystem::path install_dir = "/usr"; } system;

    config_t::config_t ( int argc, char** argv )
    {
        auto option_description = boost::program_options::options_description("options");
        option_description.add_options()
            ("--project-dir",   boost::program_options::value<std::filesystem::path>   (&this->project_dir)  ->default_value("."))
            ("--build-dir",     boost::program_options::value<std::filesystem::path>   (&this->build_dir)    ->default_value(".cppmake"))
            ("--install-dir",   boost::program_options::value<std::filesystem::path>   (&this->install_dir)  ->default_value(system.install_dir))
            // ("--compiler-path", boost::program_options::value<resolvable_path>         (&this->compiler_path)->default_value(system.compiler_path))
            // ("--compile-std",   boost::program_options::value<config_t::compile_std_t> (&this->compile_std)  ->default_value(config_t::compile_std_t::cpp26))
            // ("--compile-type",  boost::program_options::value<config_t::compile_type_t>(&this->compile_type) ->default_value(config_t::compile_type_t::debug))
            // ("--linker-path",   boost::program_options::value<resolvable_path>         (&this->linker_path)  ->default_value(system.linker_path))
            // ("--linker-type",   boost::program_options::value<config_t::link_type_t>   (&this->link_type)    ->default_value(config_t::link_type_t::static_))
            ("--target",        boost::program_options::value<std::string>             (&this->target)       ->default_value("make"))
            ("--jobs",          boost::program_options::value<unsigned>                (&this->jobs)         ->default_value(std::thread::hardware_concurrency()))
            ("--verbose",       boost::program_options::bool_switch                    (&this->verbose)      ->default_value(false))
            ("--dry",           boost::program_options::bool_switch                    (&this->dry)          ->default_value(false));

        boost::program_options::command_line_parser(argc, argv).options(option_description).run();
    }
}