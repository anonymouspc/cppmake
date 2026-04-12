export module cppmake:execution.algorighm;
import        cppmake:utility.concepts;
import        std;
import        boost.asio;

namespace cppmake
{
    auto sync_wait ( awaitable auto&& );

    awaitable auto when_all ( awaitable auto&&... );

    template < class... Ts >
    awaitable 
}