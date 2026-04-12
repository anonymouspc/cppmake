set -x

./pkg/std/make-mach.sh
./pkg/boost/make-mach.sh

mkdir -p .cppmake/import
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/utility/argv.cpp -o .cppmake/import/cppmake-utility.argv.pcm # cppmake:utility
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-utility.argv.pcm -o .cppmake/import/cppmake-utility.argv.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/utility/concepts.cpp -o .cppmake/import/cppmake-utility.concepts.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-utility.concepts.pcm -o .cppmake/import/cppmake-utility.concepts.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/utility/filesystem.cpp -o .cppmake/import/cppmake-utility.filesystem.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-utility.filesystem.pcm -o .cppmake/import/cppmake-utility.filesystem.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/utility/templates.cpp -o .cppmake/import/cppmake-utility.templates.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-utility.templates.pcm -o .cppmake/import/cppmake-utility.templates.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/utility/throws.cpp -o .cppmake/import/cppmake-utility.throws.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-utility.throws.pcm -o .cppmake/import/cppmake-utility.throws.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/utility/version.cpp -o .cppmake/import/cppmake-utility.version.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-utility.version.pcm -o .cppmake/import/cppmake-utility.version.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/error/config.cpp -o .cppmake/import/cppmake-error.config.pcm # cppmake:error
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-error.config.pcm -o .cppmake/import/cppmake-error.config.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/error/grouped.cpp -o .cppmake/import/cppmake-error.grouped.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-error.grouped.pcm -o .cppmake/import/cppmake-error.grouped.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/system/base.cpp -o .cppmake/import/cppmake-system.base.pcm # cppmake:system
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-system.base.pcm -o .cppmake/import/cppmake-system.base.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/system/linux.cpp -o .cppmake/import/cppmake-system.linux.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-system.linux.pcm -o .cppmake/import/cppmake-system.linux.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/system/mach.cpp -o .cppmake/import/cppmake-system.mach.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-system.mach.pcm -o .cppmake/import/cppmake-system.mach.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/system/win32.cpp -o .cppmake/import/cppmake-system.win32.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-system.win32.pcm -o .cppmake/import/cppmake-system.win32.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/system/all.cpp -o .cppmake/import/cppmake-system.all.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-system.all.pcm -o .cppmake/import/cppmake-system.all.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/basic/config.cpp -o .cppmake/import/cppmake-basic.config.pcm # cppmake:basic
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-basic.config.pcm -o .cppmake/import/cppmake-basic.config.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake.cpp -o .cppmake/import/cppmake.pcm # cppmake
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake.pcm -o .cppmake/import/cppmake.o

mkdir -p .cppmake/bin
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c bin/main.cpp -o .cppmake/bin/main.o
clang++ -rdynamic .cppmake/bin/main.o .cppmake/import/*.o .cppmake/pkg/std/import/*.o .cppmake/pkg/boost/import/*.o .cppmake/pkg/boost/lib/*.a -o .cppmake/bin/main

