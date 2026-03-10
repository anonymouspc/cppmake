#include <concepts>

namespace cppmake
{
    template < class... Types >
    void template_for ( auto&& function )
        requires (requires {function.template operator()<Types>(); } and ...);
}