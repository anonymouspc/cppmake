#pragma once
#include <cppmakelib/utility/concept.hpp>
#include <exception>
#include <ranges>
#include <vector>

namespace cppmake
{
    template < class Exception >
    class __grouped_exception
      : public Exception
    {
        public:
            __grouped_exception ( iterable_as<Exception> auto&& );
        
        public:
            virtual const char* what ( ) const noexcept override;

        private:
            std::string message;
    };



    template < class Exception >
    __grouped_exception<Exception>::__grouped_exception ( iterable_as<Exception> auto&& exceptions )
      : Exception(*std::ranges::begin(exceptions)),
        message
            (
                exceptions | std::views::transform([] (const Exception& exception) { return std::string_view(exception.what()); }) 
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

    auto a = __grouped_exception<std::exception>(std::vector<std::exception>());



}