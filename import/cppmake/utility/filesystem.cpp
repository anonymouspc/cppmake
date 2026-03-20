export module cppmake:utility.filesystem;
import        std;
import        boost.process;

namespace cppmake
{
    export class absolute_path
      : public std::filesystem::path
    {
        public:
            absolute_path ( )                       = default;
            absolute_path ( const char* );
            absolute_path ( std::filesystem::path );
    };

    export class relative_path
      : public std::filesystem::path
    {
        public:
            relative_path ( )                       = default;
            relative_path ( const char* );
            relative_path ( std::filesystem::path );
    };

    export class resolvable_path
    {
        public:
            resolvable_path ( )             = default;
            resolvable_path ( const char* );
            resolvable_path ( std::string );

        public:
            std::string data;
            friend std::filesystem::path resolve ( const resolvable_path& );
            friend std::istream& operator >> ( std::istream&,       resolvable_path& );
            friend std::ostream& operator << ( std::ostream&, const resolvable_path& );
    };



    absolute_path::absolute_path ( const char* path )
      : absolute_path(std::filesystem::path(path))
    {

    }

    absolute_path::absolute_path ( std::filesystem::path path )
      : std::filesystem::path(std::move(path))
    {

    }

    relative_path::relative_path ( const char* path )
      : relative_path(std::filesystem::path(path))
    {

    }

    relative_path::relative_path ( std::filesystem::path path )
      : std::filesystem::path(std::move(path))
    {

    }

    resolvable_path::resolvable_path ( const char* path )
      : resolvable_path(std::filesystem::path(path))
    {

    }
    
    resolvable_path::resolvable_path ( std::string path )
      : data(std::move(path))
    {
        
    }

    std::filesystem::path resolve ( const resolvable_path& path )
    {
        return boost::process::environment::find_executable(path.data);
    }

    std::istream& operator >> ( std::istream& left, resolvable_path& right )
    {
        return left >> right.data;
    }

    std::ostream& operator << ( std::ostream& left, const resolvable_path& right )
    {
        return left << right.data;
    }
}