#include <print>
#include <boost/program_options.hpp>

int main ( int argc, char** argv )
{
    int value = 0;
    auto descreption = boost::program_options::options_description("options");
    descreption.add_options()
        ("value", boost::program_options::value<int>(&value)->default_value(42));
    auto options = boost::program_options::command_line_parser(argc, argv).options(descreption).run();
    auto variables_map = boost::program_options::variables_map();
    boost::program_options::store(options, variables_map);
    boost::program_options::notify(variables_map);
    std::println("value={}", value);
}