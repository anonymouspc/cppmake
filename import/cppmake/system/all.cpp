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
    export std::variant<linux, mach, win32> system = [] 
        {
            auto values = std::list<std::variant<linux, mach, win32>>();
            auto errors = std::list<config_error>();

            template_for<linux, mach, win32>([&] <class System>
            {
                try
                {
                    values.push_back(System());
                }
                catch (config_error& error)
                {
                    errors.push_back(std::move(error));
                }
            });

            if (values.size() == 0)
                throw_with_nested
                (
                    config_error("system is not recognized"), 
                    grouped_exception<config_error>(errors)
                );
            else if (values.size() == 1)
                return std::move(*values.begin());
            else // if (values.size() >= 2)
                throw_with_nested
                (
                    config_error("system is ambiguous"), 
                    grouped_exception<config_error>(
                        values | std::views::transform([] (auto&& value) 
                            { 
                                return config_error(std::format("{} is satisfied", value.visit([] (auto&& system) { return system.name; }))); 
                            }))
                );
        } ();
}
