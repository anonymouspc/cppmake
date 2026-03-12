#pragma once
#include <stdexcept>

namespace cppmake
{
    class config_error 
        : public std::runtime_error
    {
        using std::runtime_error::runtime_error;
    };
}