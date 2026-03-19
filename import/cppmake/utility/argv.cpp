export module cppmake:utility.argv;

namespace cppmake 
{
    export extern int    argc;
    export extern char** argv;
}



#ifdef __linux__
    extern "C" int    __libc_argc;
    extern "C" char** __libc_argv;
    int    cppmake::argc = __libc_argc;
    char** cppmake::argv = __libc_argv;
#elifdef __MACH__
    extern "C" int*    _NSGetArgc();
    extern "C" char*** _NSGetArgv();
    int    cppmake::argc = *_NSGetArgc();
    char** cppmake::argv = *_NSGetArgv();
#elifdef _WIN32
    extern "C" int    __argc;
    extern "C" char** __argv;
    int    cppmake::argc = __argc;
    char** cppmake::argv = __argv;
#else
    #error "system not supported"
#endif