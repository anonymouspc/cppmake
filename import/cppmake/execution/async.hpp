module;
#include <version>

export module cppmake.execution.async;
import        std;
import        boost.asio;

namespace cppmake
{
    #ifdef __cpp_lib_sender
        export template < class T, class V >
        concept async = std::execution::sender<T>;
        export template < class V >
        using co_async = std::execution::task<V>;
    #else
        export template < class T, class V >
        concept async = std::convertible_to<T, boost::asio::awaitable<V>>;
        export template < class V >
        using co_async = boost::asio::awaitable<V>;
    #endif
}