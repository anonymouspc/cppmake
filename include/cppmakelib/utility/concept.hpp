#include <concepts>
#include <ranges>

namespace cppmake
{
    template < class T, class V = void >
    concept iterable = std::ranges::range<T> and (std::convertible_to<std::ranges::range_value_t<T>, V> or std::same_as<V, void>);
};  