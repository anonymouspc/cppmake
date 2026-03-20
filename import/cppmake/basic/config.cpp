export module cppmake:basic.config;
import               :error.config;
import               :system.all;
import               :utility.argv;
import               :utility.filesystem;
import        std;
import        boost.program_options;



namespace cppmake
{
    export class config_t
    {
        public:
            enum class compile_std_t  { cpp20, cpp23, cpp26 };
            enum class compile_type_t { debug, release, size };
            enum class link_type_t    { static_, dynamic };

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
            config_t ( int argc, char** argv );
    };

    export extern config_t config;

    

    std::istream& operator >> ( std::istream& left, config_t::compile_std_t& right )
    {
        std::string compile_std_string;
        left >> compile_std_string;
        right = (compile_std_string == "c++20") ? config_t::compile_std_t::cpp20 :
                (compile_std_string == "c++23") ? config_t::compile_std_t::cpp23 :
                (compile_std_string == "c++26") ? config_t::compile_std_t::cpp26 :
                                                  throw config_error("invalid compile std");
        return left;
    }

    export std::ostream& operator << ( std::ostream& left, const config_t::compile_std_t& right )
    {
        std::string compile_std_string = (right == config_t::compile_std_t::cpp20) ? "c++20" : 
                                         (right == config_t::compile_std_t::cpp23) ? "c++23" :       
                                         (right == config_t::compile_std_t::cpp26) ? "c++26" :
                                                                                     throw config_error("invalid compile std");
        left << compile_std_string;
        return left;
    }

    std::istream& operator >> ( std::istream& left, config_t::compile_type_t& right )
    {
        std::string compile_type_string;
        left >> compile_type_string;
        right = (compile_type_string == "debug")   ? config_t::compile_type_t::debug   :
                (compile_type_string == "release") ? config_t::compile_type_t::release :
                (compile_type_string == "size")    ? config_t::compile_type_t::size    :
                                                     throw config_error("invalid compile type");
        return left;
    }

    std::ostream& operator << ( std::ostream& left, const config_t::compile_type_t& right )
    {
        std::string compile_type_string = (right == config_t::compile_type_t::debug)   ? "debug"   :
                                          (right == config_t::compile_type_t::release) ? "release" :
                                          (right == config_t::compile_type_t::size)    ? "size"    :
                                                                                         throw config_error("invalid compile type");
        left << compile_type_string;
        return left;
    }

    std::istream& operator >> ( std::istream& left, config_t::link_type_t& right )
    {
        std::string link_type_string;
        left >> link_type_string;
        right = (link_type_string == "static")  ? config_t::link_type_t::static_ :
                (link_type_string == "dynamic") ? config_t::link_type_t::dynamic :
                                                  throw config_error("invalid link type");
        return left;
    }

    std::ostream& operator << ( std::ostream& left, const config_t::link_type_t& right )
    {
        std::string link_type_string = (right == config_t::link_type_t::static_) ? "static"  :
                                       (right == config_t::link_type_t::dynamic) ? "dynamic" :
                                                                                   throw config_error("invalid link type");
        left << link_type_string;
        return left;
    }

    config_t::config_t ( int argc, char** argv )
    {
        auto option_description = boost::program_options::options_description("options");
        option_description.add_options()
            ("project-dir",   boost::program_options::value<std::filesystem::path>   (&this->project_dir)  ->default_value("."))
            ("build-dir",     boost::program_options::value<std::filesystem::path>   (&this->build_dir)    ->default_value(".cppmake"))
            ("install-dir",   boost::program_options::value<std::filesystem::path>   (&this->install_dir)  ->default_value(system.install_dir))
            ("compiler-path", boost::program_options::value<resolvable_path>         (&this->compiler_path)->default_value(system.compiler_path))
            ("compile-std",   boost::program_options::value<config_t::compile_std_t> (&this->compile_std)  ->default_value(config_t::compile_std_t::cpp26))
            ("compile-type",  boost::program_options::value<config_t::compile_type_t>(&this->compile_type) ->default_value(config_t::compile_type_t::debug))
            ("linker-path",   boost::program_options::value<resolvable_path>         (&this->linker_path)  ->default_value(system.linker_path))
            ("linker-type",   boost::program_options::value<config_t::link_type_t>   (&this->link_type)    ->default_value(config_t::link_type_t::static_))
            ("target",        boost::program_options::value<std::string>             (&this->target)       ->default_value("make"))
            ("jobs",          boost::program_options::value<unsigned>                (&this->jobs)         ->default_value(std::thread::hardware_concurrency()))
            ("verbose",       boost::program_options::bool_switch                    (&this->verbose)      ->default_value(false))
            ("dry",           boost::program_options::bool_switch                    (&this->dry)          ->default_value(false));

        auto options = boost::program_options::command_line_parser(argc, argv).options(option_description).run();
        auto variables = boost::program_options::variables_map();
        boost::program_options::store(options, variables);
        boost::program_options::notify(variables);
    }

    config_t config = config_t(argc, argv);
}