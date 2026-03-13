#pragma once

namespace cppmake 
{
    extern int    argc;
    extern char** argv;
}



#ifdef __linux__
    extern int    __libc_argc;
    extern char** __libc_argv;
    int    cppmake::argc = __libc_argc;
    char** cppmake::argv = __libc_argv;
#elifdef __MACH__
    extern int*    _NSGetArgc();
    extern char*** _NSGetArgv();
    int    cppmake::argc = *_NSGetArgc();
    char** cppmake::argv = *_NSGetArgv();
#elifdef _WIN32
    extern int    __argc;
    extern char** __argv;
    int    cppmake::argc = __argc;
    char** cppmake::argv = __argv;
#else
    #error "system not supported"
#endif