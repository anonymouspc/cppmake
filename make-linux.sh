# pkg/std
mkdir -p .cppmake/pkg/std/install/import
echo "std .cppmake/pkg/std/install/import/std.gcm" > .cppmake/pkg/std/install/import/g++-mapper.txt
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/pkg/std/install/import/g++-mapper.txt -c $(find $(dirname $(which g++))/.. | grep "std.cc" | head -n 1) -o .cppmake/import/std.o

# pkg/boost
cd pkg/boost
./bootstrap.sh
./b2 --with-process --with-program_options --build-dir=../../.cppmake/pkg/boost/build --prefix=../../.cppmake/pkg/boost/install link=static install
cd ../..

# include
cp -rl include .cppmake/include

# import
mkdir -p .cppmake/import
echo "cppmake .cppmake/import/cppmake.gcm"             >  .cppmake/import/g++-mapper.txt
echo "std     .cppmake/pkg/std/install/import/std.gcm" >> .cppmake/import/g++-mapper.txt
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/import/g++-mapper.txt -I.cppmake/include -I.cppmake/pkg/boost/install/include -Wno-expose-global-module-tu-local -c import/cppmake.cpp -o .cppmake/import/cppmake.o

# lib
mkdir -p .cppmake/lib
g++ -shared .cppmake/import/cppmake.o .cppmake/pkg/std/install/import/*.o .cppmake/pkg/boost/install/lib/*.a -o .cppmake/lib/cppmake.so

# bin
mkdir -p .cppmake/bin
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/import/g++-mapper.txt -c bin/main.cpp -o .cppmake/bin/main.o
g++ .cppmake/bin/main.o .cppmake/lib/cppmake.so -o .cppmake/bin/main
