set -x

mkdir -p .cppmake/import
echo "cppmake:utility.argv .cppmake/import/cppmake-utility.argv.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/utility/argv.cpp -o .cppmake/import/cppmake-utility.argv.o
echo "cppmake .cppmake/import/cppmake.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake.cpp -o .cppmake/import/cppmake.o


mkdir -p .cppmake/bin
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c bin/main.cpp -o .cppmake/bin/main.o
g++ -rdynamic .cppmake/bin/main.o .cppmake/import/*.o .cppmake/pkg/std/import/*.o .cppmake/pkg/boost/import/*.o .cppmake/pkg/boost/lib/*.a -o .cppmake/bin/main
