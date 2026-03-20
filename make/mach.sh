set -x

mkdir -p .cppmake/import
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/utility/argv.cpp -o .cppmake/import/cppmake-utility.argv.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-utility.argv.pcm -o .cppmake/import/cppmake-utility.argv.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/utility/concepts.cpp -o .cppmake/import/cppmake-utility.concepts.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-utility.concepts.pcm -o .cppmake/import/cppmake-utility.concepts.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/utility/filesystem.cpp -o .cppmake/import/cppmake-utility.filesystem.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-utility.filesystem.pcm -o .cppmake/import/cppmake-utility.filesystem.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/utility/templates.cpp -o .cppmake/import/cppmake-utility.templates.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-utility.templates.pcm -o .cppmake/import/cppmake-utility.templates.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake/utility/version.cpp -o .cppmake/import/cppmake-utility.version.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake-utility.version.pcm -o .cppmake/import/cppmake-utility.version.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import --precompile -x c++-module import/cppmake.cpp -o .cppmake/import/cppmake.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/import/cppmake.pcm -o .cppmake/import/cppmake.o

mkdir -p .cppmake/bin
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import -fprebuilt-module-path=.cppmake/pkg/std/import -fprebuilt-module-path=.cppmake/pkg/boost/import -c bin/main.cpp -o .cppmake/bin/main.o
clang++ -rdynamic .cppmake/bin/main.o .cppmake/import/*.o .cppmake/pkg/std/import/*.o .cppmake/pkg/boost/import/*.o .cppmake/pkg/boost/lib/*.a -o .cppmake/bin/main
