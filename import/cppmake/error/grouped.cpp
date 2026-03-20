export module cppmake:error.grouped;
import               :utility.concepts;
import        std;

namespace cppmake
{
    export template < class Exception >
    class grouped_exception
      : public Exception
    {
        public:
            grouped_exception ( iterable_as<Exception> auto&& );
        
        public:
            virtual const char* what ( ) const noexcept override;

        private:
            std::string message;
    };



    template < class Exception >
    grouped_exception<Exception>::grouped_exception ( iterable_as<Exception> auto&& exceptions )
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
    const char* grouped_exception<Exception>::what ( ) const noexcept
    {
        return message.c_str();
    }
}