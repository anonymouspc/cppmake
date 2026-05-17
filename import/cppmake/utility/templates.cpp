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

    template < class Base, class... Deriveds >
        requires (std::derived_from<Deriveds, Base> and ...)
    std::unique_ptr<Base> select_unique ( auto&&... construct_arguments )
    {
        auto values = std::vector<std::unique_ptr<Base>>();
        auto errors = std::vector<std::exception_ptr>();

        template_for<Deriveds...>([&] <class Derived>
            {
                try
                {
                    values.emplace_back(std::make_unique<Derived>(std::forward<decltype(construct_arguments)>(construct_arguments)...));
                }
                catch (...)
                {
                    errors.push_back(std::current_exception());
                }
            });
    }
    
}