#include <cppmake/system/linux.hpp>
#include <cppmake/system/mach.hpp>
#include <cppmake/system/win32.hpp>
#include <cppmake/utility/template.hpp>

namespace cppmake
{
    class any_system
    {
        public:
            std::string executable_suffix;
            std::string object_suffix;
            s

        public:
            any_system ( auto&& );
    };

    any_system system = []
    {
        auto matches = std::vector<any_system>();
        template_for<linux,mach,win32>([&] <class System> 
        { 
            matches.push_back(System()); 
        });
        if (matches.size() == 0)
            throw config_error("system is not recognized"); // add suberror
        else if (matches.size() == 1)
            return matches[0];
        else // if (recognized_systems.size() >= 2)
            throw config_error("system is ambiguous");

    } ();

}
