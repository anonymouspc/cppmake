#include <concepts>
#include <ranges>

namespace cppmake
{
    template < class T, class V >
    concept iterable_as = requires (T t) { { *std::begin(t) } -> std::convertible_to<V>; };

    template < class T, class K, class V >
    concept mappable_as = requires (T t, K k) { { t[k] } -> std::convertible_to<V>; };
};  