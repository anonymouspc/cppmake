#pragma once
#include <memory>
#include <vector>
#include <cppmake/error/config.hpp>
#include <cppmake/system/base.hpp>
#include <cppmake/system/linux.hpp>
#include <cppmake/system/mach.hpp>
#include <cppmake/system/win32.hpp>
#include <cppmake/utility/template.hpp>

namespace cppmake
{
    extern system_t& system;

    

    auto system_ptr = []
        {
            auto values = std::vector<std::unique_ptr<system_t>>();
            template_for<linux, mach, win32>([&] <class System>
                {
                    try { values.push_back(std::make_unique<System>()); } catch (const config_error& error) { }
                });
            if (values.size() == 0)
                throw config_error("system is not recognized");
            else if (values.size() == 1)
                return std::move(values[0]);
            else // if (values.size() >= 2 )
                throw config_error("system is ambiguous");
        } ();

    system_t& system = *system_ptr;
}
