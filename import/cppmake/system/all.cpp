export module cppmake:system.all;
import               :system.linux;
import               :system.mach;
import               :system.win32;
import               :error.config;
import               :error.grouped;
import               :utility.templates;
import               :utility.throws;
import        std;

namespace cppmake
{
    export extern system_t& system;

    

    auto system_ptr = []
        {
            auto value_ptrs = std::vector<std::unique_ptr<system_t>>();
            auto errors     = std::vector<config_error>();

            template_for<linux, mach, win32>([&] <class System>
                {
                    try 
                    { 
                        value_ptrs.push_back(std::make_unique<System>()); 
                    } 
                    catch (config_error& error) 
                    { 
                        errors.push_back(std::move(error)); 
                    }
                });

            if (value_ptrs.size() == 0)
                throw_with_nested
                (
                    config_error("system is not recognized"), 
                    grouped_exception<config_error>(errors)
                );
            else if (value_ptrs.size() == 1)
                return std::move(value_ptrs[0]);
            else // if (values.size() >= 2)
                throw_with_nested
                (
                    config_error("system is ambiguous"), 
                    grouped_exception<config_error>(value_ptrs | std::views::transform([] (auto&& value_ptr) { return config_error(std::format("{} is available", value_ptr->name)); }))
                );
        } ();

    system_t& system = *system_ptr;
}
