#include <ranges>
#include <vector>
#include <cppmakelib/error/any.hpp>
#include <cppmakelib/utility/concept.hpp>

namespace cppmake
{
    template < class Exception >
    class __grouped_exception
        : public Exception
    {
        public:
            __grouped_exception ( iterable<Exception> auto&& );
        
        public:
            virtual const char* what ( ) const noexcept override;

        private:
            std::string message;
    };



    template < class Exception >
    __grouped_exception<Exception>::__grouped_exception ( iterable<Exception> auto&& exceptions )
      : Exception(*std::ranges::begin(exceptions)),
        message
            (
                exceptions | std::ranges::transform([] (Exception&& exception) { return std::string_view(exception.what()); }) 
                           | std::views::join_with('\n') 
                           | std::ranges::to<std::string>()
            )
    {
        
    }

    template < class Exception >
    const char* __grouped_exception<Exception>::what ( ) const noexcept
    {
        return message.c_str();
    }



}