set -x

mkdir -p .cppmake/import
echo "cppmake.utility.argv .cppmake/import/cppmake.utility.argv.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/utility/argv.cpp -o .cppmake/import/cppmake.utility.argv.o
echo "cppmake.error.config .cppmake/import/cppmake.error.config.gcm" >> ".cppmake/.mapper"
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -c import/cppmake/error/config.cpp -o .cppmake/import/cppmake.error.config.o
