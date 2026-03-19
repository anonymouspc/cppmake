export module cppmake:utility.argv;

namespace cppmake 
{
    export extern int    argc;
    export extern char** argv;
}



#ifdef __linux__
    int    cppmake::argc;
    char** cppmake::argv;
    [[gnu::constructor]]
    void constructor ( int argc, char** argv )
    {
        cppmake::argc = argc;
        cppmake::argv = argv;
    }
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