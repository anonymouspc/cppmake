module;
#include <boost/program_options.hpp>

export module boost.program_options;

namespace boost::program_options
{
    export using boost::program_options::bool_switch;
    export using boost::program_options::command_line_parser;
    export using boost::program_options::options_description;
    export using boost::program_options::store;
    export using boost::program_options::value;
}