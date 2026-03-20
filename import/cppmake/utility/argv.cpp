export module cppmake:utility.argv;
import        std;

namespace cppmake 
{
    extern int    argc;
    extern char** argv;



    #ifdef __linux__
        extern "C" [[gnu::weak]] int    __libc_argc;
        extern "C" [[gnu::weak]] char** __libc_argv;
        int    argc = __libc_argc;
        char** argv = __libc_argv;
    #elifdef __MACH__
        extern "C" int*    _NSGetArgc();
        extern "C" char*** _NSGetArgv();
        int argc    = *_NSGetArgc();
        char** argv = *_NSGetArgv();
    #elifdef _MSC_VER
        extern "C" int    __argc;
        extern "C" char** __argv;
        int    argc = __argc;
        char** argv = __argv;
    #else
        #error "compiler not supported"
    #endif
}



