#include <cppmake/system/
#include <cppmake/system/base.hpp>
#include <cppmake/system/linux.hpp>
#include <cppmake/system/mach.hpp>
#include <cppmake/system/win32.hpp>
#include <cppmake/utility/template.hpp>
#include <memory>
#include <vector>

namespace cppmake
{
    auto system_ptr = []
        {
            auto system_candidate_ptrs = std::vector<std::unique_ptr<system>>();
            auto errors = std::vector<std::unique_ptr<config_error>>();
            template_for<linux, mach, win32>([&] <class System>
                {
                    try
                    {
                        system_candidate_ptrs.push_back(System());
                    }
                    catch (const std::runtime_error& error)
                    {
                        
                    }
                }
        }


    auto system_ptr = std::make_unique<system>([]
        {
            
        });

    system& system = *system_ptr;
    
    
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
