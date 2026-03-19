#pragma once
#include <cppmakelib/error/config.hpp>
#include <cppmakelib/error/grouped.hpp>
#include <cppmakelib/system/base.hpp>
#include <cppmakelib/system/linux.hpp>
#include <cppmakelib/system/mach.hpp>
#include <cppmakelib/system/win32.hpp>
#include <cppmakelib/utility/template.hpp>
#include <exception>
#include <memory>
#include <vector>

namespace cppmake
{
    extern system_t& system;

    

    auto __system_ptr = []
        {
            auto value_ptrs = std::vector<std::unique_ptr<system_t>>();
            auto error_ptrs = std::vector<std::exception_ptr>();

            template_for<linux, mach, win32>([&] <class System>
                {
                    try 
                    { 
                        value_ptrs.push_back(std::make_unique<System>()); 
                    } 
                    catch (const config_error& error) 
                    { 
                        error_ptrs.push_back(std::make_exception_ptr(error)); 
                    }
                });

            if (value_ptrs.size() == 0)
                try 
                { 
                    throw __grouped_exception<config_error>(error_ptrs | std::views::transform([] (auto&& error_ptr) { try { std::rethrow_exception(error_ptr); } catch (const config_error& error) { return error; } })); 
                } 
                catch (...) 
                { 
                    std::throw_with_nested(config_error("system is not recognized")); 
                }
            else if (value_ptrs.size() == 1)
                return std::move(value_ptrs[0]);
            else // if (values.size() >= 2 )
                try 
                { 
                    throw __grouped_exception<config_error>(value_ptrs | std::views::transform([] (auto&& value_ptr) { return config_error(std::format("{} is available", value_ptr->name)); }));
                } 
                catch (...)
                {
                    std::throw_with_nested(config_error("system is ambiguous"));
                }
        } ();

    system_t& system = *__system_ptr;
}
