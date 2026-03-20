export module cppmake:utility.concepts;
import        std;

namespace cppmake
{
    export template < class T, class V >
    concept iterable_as = requires (T t) { { *std::begin(t) } -> std::convertible_to<V>; };

    export template < class T, class K, class V >
    concept mappable_as = requires (T t, K k) { { t[k] } -> std::convertible_to<V>; };
};  