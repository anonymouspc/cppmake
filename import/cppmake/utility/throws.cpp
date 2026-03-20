export module cppmake:utility.throws;
import        std;

namespace cppmake
{
    [[noreturn]] void throw_with_nested ( auto&& exception, auto&& nested_exception ) 
    {
        try
        {
            throw std::forward<decltype(nested_exception)>(nested_exception);
        }
        catch (...)
        {
            std::throw_with_nested(std::forward<decltype(exception)>(exception));
        }
    }
}