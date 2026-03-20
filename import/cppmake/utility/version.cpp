export module cppmake:utility.version;
import               :utility.concepts;

namespace cppmake
{
    export class version_t;
    export extern version_t version;


    
    class version_t
    {
        version_t ( const iterable_as<int> auto& );
    };
}