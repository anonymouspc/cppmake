export module cppmake:execution.run;
import               :basic.config;
import               :utility.concepts;
import               :utility.filesystem;
import        std;
import        boost.asio;
import        boost.process;

namespace cppmake
{
    export void async_run 
    ( 
        const resolvable_path&                                file, 
        const iterable_as<std::string> auto&                  args          = {}, 
        const std::filesystem::path&                          cwd           = std::filesystem::current_path(),
        const indexable_into<std::string, std::string>  auto& env           = boost::process::environment::current() | std::ranges::to<std::map<std::string, std::string>>(),   
        bool                                                  print_command = config.verbose,
        bool                                                  print_stdout  = config.verbose,
        bool                                                  print_stderr  = config.verbose,
        std::optional<std::string&>                           store_stdout  = std::nullopt,
        std::optional<std::string&>                           store_stderr  = std::nullopt,
    );
}