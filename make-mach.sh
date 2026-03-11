# Make packages
(
    cd pkg/boost
    ./bootstrap.sh
    ./b2 --with-process --with-program_options --build-dir=../../.cppmake/pkg/boost/build --prefix=../../.cppmake/pkg/boost/install link=static install
)

# Make cppmake
mkdir -p .cppmake/bin
clang++ -std=c++26 -Iinclude -I.cppmake/pkg/boost/install/include -x c++-modules import/cppmake.cpp -o .cppmake/import/cppmake.pcm
clang++ .cppmake/import/cppmake.pcm -o .cppmake/import/cppmake.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/import bin/main.cpp -o .cppmake/bin/main.o 
clang++ .cppmake/bin/main.o .cppmake/import/cppmake.o .cppmake/pkg/boost/install/lib/*.a -o .cppmake/bin/main