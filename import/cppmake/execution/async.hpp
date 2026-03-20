export module cppmake.execution.async;
import        boost.asio;

namespace cppmake
{
    export template < class T >
    using co_async = boost::asio::awaitable;
}