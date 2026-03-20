export module cppmake:utility.templates;
import        std;

namespace cppmake
{
    template < class... Ts >
    void template_for ( auto&& function )
        requires (requires {function.template operator()<Ts>(); } and ...);



    void template_for_impl ( auto&& function )
    {
        
    }

    template < class T, class... Ts >
    void template_for_impl ( auto&& function )
    {
        function.template operator()<T>();
        template_for_impl<Ts...>(std::forward<decltype(function)>(function));
    }

    template < class... Ts >
    void template_for ( auto&& function )
        requires (requires {function.template operator()<Ts>(); } and ...)
    {
        template_for_impl<Ts...>(std::forward<decltype(function)>(function));
    }
}