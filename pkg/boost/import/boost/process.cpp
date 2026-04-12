module;
#define BOOST_PROCESS_USE_STD_FS
#include <boost/process.hpp>

export module boost.process;

namespace boost::process
{
    export using boost::process::process;

    namespace environment
    {
        export using boost::process::environment::find_executable;
        export using boost::process::environment::current;
    }
}