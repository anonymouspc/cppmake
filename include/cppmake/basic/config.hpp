#include <filesystem>
#include <string>
#include <boost/asio.hpp>
#include <boost/program_options.hpp>

namespace cppmake
{
    namespace config
    {
        enum class std_t  { cpp20, cpp23, cpp26 };
        enum class type_t { debug, release, size };

        std::filesystem::path project;
        std::string           target;
        std::filesystem::path compiler;
        std_t                 std;
        type_t                type;
        unsigned              jobs;
        bool                  verbose;
        std::filesystem::path build_dir;
        std::filesystem::path install_dir;
    }

    auto positional_parser = boost::program_options::positional_options_description().add
        ("project", 1);
    auto sorted_parser     = boost::program_options::options_description("options").add_options()
        ("target",      boost::program_options::value<std::string>          (&config::target)     ->default_value("."),                                 "select make target")
        ("compiler",    boost::program_options::value<std::filesystem::path>(&config::compiler)   ->default_value(system.compiler),                     "use specific C++ compiler")
        ("std",         boost::program_options::value<config::std_t>        (&config::std)        ->default_value(config::std_t::cpp26),                "use specific C++ standard")
        ("type",        boost::program_options::value<config::type_t>       (&config::type)       ->default_value(config::type_t::debug) ,              "choose config type")
        ("jobs",        boost::program_options::value<unsigned>             (&config::jobs)       ->default_value(std::thread::hardware_concurrency()), "allow maximun concurrency")
        ("verbose",     boost::program_options::bool_switch                 (&config::verbose)    ->default_value(false),                               "print verbose outputs")
        ("build-dir",   boost::program_options::value<std::filesystem::path>(&config::build_dir)  ->default_value(".cppmake"),                          "specify build dir")
        ("install-dir", boost::program_options::value<std::filesystem::path>(&config::install_dir)->default_value(system.install_dir),                  "specify install dir");
    
}