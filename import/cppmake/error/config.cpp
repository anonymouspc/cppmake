export module cppmake.error.config;
import        std;

namespace cppmake
{
    export class config_error
      : public std::runtime_error
    {
        using std::runtime_error::runtime_error;
    };
}