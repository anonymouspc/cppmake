# Make packages
cd pkg/boost
./bootstrap.sh
./b2 --with-process --with-program_options --build-dir=../../.cppmake/pkg/boost/build --prefix=../../.cppmake/pkg/boost/install link=static install
cd ../..

# Make cppmake
mkdir -p .cppmake/bin
clang++ -std=c++26 -Iinclude -I.cppmake/pkg/boost/install/include -x c++ bin/main.cpp .cppmake/pkg/boost/install/lib/*.a -o .cppmake/bin/main
clang++ -std=c++26 -Iinclude -I.cppmake/pkg/boost/install/include -x c++-modules import/cppmake.cpp -o .cppmake/import/cppmake.pcm
clang++ .cppmake/import/cppmake.pcm -o .cppmake/import/cppmake.o
clang++ -shared .cppmake/import/cppmake.o .cppmake/pkg/boost/install/lib/*.a -o .cppmake/lib/cppmake.dylib
