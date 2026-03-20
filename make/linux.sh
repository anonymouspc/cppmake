set -x

mkdir -p .cppmake/import
echo "cppmake:utility.argv .cppmake/import/cppmake-utility.argv.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/utility/argv.cpp -o .cppmake/import/cppmake-utility.argv.o
echo "cppmake:utility.concepts .cppmake/import/cppmake-utility.concepts.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/utility/concepts.cpp -o .cppmake/import/cppmake-utility.concepts.o
echo "cppmake:utility.filesystem .cppmake/import/cppmake-utility.filesystem.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/utility/filesystem.cpp -o .cppmake/import/cppmake-utility.filesystem.o
echo "cppmake:utility.templates .cppmake/import/cppmake-utility.templates.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/utility/templates.cpp -o .cppmake/import/cppmake-utility.templates.o
echo "cppmake:utility.throws .cppmake/import/cppmake-utility.throws.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/utility/throws.cpp -o .cppmake/import/cppmake-utility.throws.o
echo "cppmake:utility.version .cppmake/import/cppmake-utility.version.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/utility/version.cpp -o .cppmake/import/cppmake-utility.version.o
echo "cppmake:error.config .cppmake/import/cppmake-error.config.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/error/config.cpp -o .cppmake/import/cppmake-error.config.o
echo "cppmake:error.grouped .cppmake/import/cppmake-error.grouped.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/error/grouped.cpp -o .cppmake/import/cppmake-error.grouped.o
echo "cppmake:system.base .cppmake/import/cppmake-system.base.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/system/base.cpp -o .cppmake/import/cppmake-system.base.o
echo "cppmake:system.linux .cppmake/import/cppmake-system.linux.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/system/linux.cpp -o .cppmake/import/cppmake-system.linux.o
echo "cppmake:system.mach .cppmake/import/cppmake-system.mach.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/system/mach.cpp -o .cppmake/import/cppmake-system.mach.o
echo "cppmake:system.win32 .cppmake/import/cppmake-system.win32.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/system/win32.cpp -o .cppmake/import/cppmake-system.win32.o
echo "cppmake:system.all .cppmake/import/cppmake-system.all.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/system/all.cpp -o .cppmake/import/cppmake-system.all.o
echo "cppmake:basic.config .cppmake/import/cppmake-basic.config.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/basic/config.cpp -o .cppmake/import/cppmake-basic.config.o
echo "cppmake .cppmake/import/cppmake.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake.cpp -o .cppmake/import/cppmake.o


mkdir -p .cppmake/bin
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c bin/main.cpp -o .cppmake/bin/main.o
g++ -rdynamic .cppmake/bin/main.o .cppmake/import/*.o .cppmake/pkg/std/import/*.o .cppmake/pkg/boost/import/*.o .cppmake/pkg/boost/lib/*.a -o .cppmake/bin/main
