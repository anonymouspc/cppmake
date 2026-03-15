# pkg/std
mkdir -p .cppmake/pkg/std/install/import
clang++ -std=c++26 -Wno-reserved-module-identifier -c $(clang++ --print-resource-dir)/../../../share/libc++/v1/std.cppm -o .cppmake/pkg/std/install/import/std.pcm

# pkg/boost
mkdir -p .cppmake/pkg/boost
cd pkg/boost
./bootstrap.sh
./b2 --with-process --with-program_options --build-dir=../../.cppmake/pkg/boost/build --prefix=../../.cppmake/pkg/boost/install link=static install
cd ../..

# include
cp -rl include .cppmake/include

# import
mkdir -p .cppmake/import
clang++ -std=c++26 -I.cppmake/include -I.cppmake/pkg/std/install/include -I.cppmake/pkg/boost/install/include --precompile -x c++-module import/cppmake.cpp -o .cppmake/import/cppmake.pcm
clang++ -c .cppmake/import/cppmake.pcm -o .cppmake/import/cppmake.o

# lib
mkdir -p .cppmake/lib
clang++ -shared .cppmake/import/cppmake.o .cppmake/pkg/boost/install/lib/*.a -o .cppmake/lib/cppmake.dylib

# bin
mkdir -p .cppmake/bin
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/pkg/std/install/import -fprebuilt-module-path=.cppmake/import -c bin/main.cpp -o .cppmake/bin/main.o
clang++ .cppmake/bin/main.o .cppmake/lib/cppmake.dylib -o .cppmake/bin/main
