export module cppmake:utility.argv;
import        std;

namespace cppmake 
{
    export extern int    argc;
    export extern char** argv;



    #ifdef __GNUC__
        int    argc;
        char** argv;
        [[gnu::constructor]]
        void init_main_argc_argv ( int main_argc, char** main_argv )
        {
            argc = main_argc;
            argv = main_argv;
        }
    #elifdef _MSC_VER
        extern "C" int    __argc;
        extern "C" char** __argv;
        int    argc = __argc;
        char** argv = __argv;
    #else
        #error "compiler not supported"
    #endif
}



