#pragma once
#include <memory>
#include <vector>
#include <cppmakelib/error/config.hpp>
#include <cppmakelib/error/grouped.hpp>
#include <cppmakelib/system/base.hpp>
#include <cppmakelib/system/linux.hpp>
#include <cppmakelib/system/mach.hpp>
#include <cppmakelib/system/win32.hpp>
#include <cppmakelib/utility/template.hpp>

namespace cppmake
{
    extern system_t& system;

    

    auto system_ptr = []
        {
            auto values = std::vector<std::unique_ptr<system_t>>();
            auto errors = std::vector<config_error>();

            template_for<linux, mach, win32>([&] <class System>
                {
                    try 
                    { 
                        values.push_back(std::make_unique<System>()); 
                    } 
                    catch (const config_error& error) 
                    { 
                        errors.push_back(error); 
                    }
                });

            if (values.size() == 0)
                try 
                { 
                    throw __grouped_exception<config_error>(errors); 
                } 
                catch (...) 
                { 
                    std::throw_with_nested(config_error("system is not recognized")); 
                }
            else if (values.size() == 1)
                return std::move(values[0]);
            else // if (values.size() >= 2 )
                try 
                { 
                    throw grouped_exception<config_error>(values | std::views::transform([] (auto&& value) { return config_error(std::format("{} is available", value->name)); }));
                } 
                catch (...)
                {
                    std::throw_with_nested(config_error("system is ambiguous"));
                }
        } ();

    system_t& system = *system_ptr;
}
