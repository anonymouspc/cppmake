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
    // auto system_ptr = []
    //     {
    //         auto candidate_ptrs = std::vector<std::unique_ptr<system>>();
    //         auto errors         = std::vector<config_error>();
    //         template_for<linux, mach, win32>([&] <class System>
    //             {
    //                 try
    //                 {
    //                     candidate_ptrs.push_back(std::make_unique<System>());
    //                 }
    //                 catch (const config_error& error)
    //                 {
    //                     errors.push_back(error);
    //                 }
    //             });
    //         if (candidate_ptrs.size() == 0)
    //             throw config_error("system is not recognized");
    //         else if (candidate_ptrs.size() == 1)
    //             return candidate_ptrs[0];
    //     } ();

    // system& system = *system_ptr;

}
