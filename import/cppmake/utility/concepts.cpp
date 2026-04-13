export module cppmake:utility.concepts;
import        std;
import        boost.asio;

namespace cppmake
{
    template < class T >
    concept iterable = 
        requires (T& t) { [] { for (auto&& v : t) return v; } (); };

    template < class T, class V >
    concept iterable_as = 
        requires (T& t) { { [] { for (auto&& v : t) return v; } () } -> std::convertible_to<V>; };

    template < class T, class I >
    concept mappable_by = 
        requires (T& t, I& i) { t[i]; };

    template < class T, class I, class V >
    concept mappable_into = 
        requires (T& t, I& i) { { t[i] } -> std::convertible_to<V>; };

    template < class T >
    concept awaitable = 
        requires (T& t) { t.await_resume(); }; // TODO: Update into sender.

    template < class T, class V >
    concept awaitable_as =
        requires (T& t) { { t.await_resume() } -> std::convertible_to<V>; };
};  