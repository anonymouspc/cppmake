module;
#define BOOST_DLL_USE_STD_FS
#include <boost/dll.hpp>
#include <boost/dll/smart_library.hpp>

export module boost.dll;

namespace boost::dll
{
    export using boost::dll::experimental::smart_library;
}