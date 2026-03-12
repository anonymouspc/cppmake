export LANG=C

# pkg
# cd pkg/boost
# ./bootstrap.sh
# ./b2 --with-process --with-program_options --build-dir=../../.cppmake/pkg/boost/build --prefix=../../.cppmake/pkg/boost/install link=static install
# cd ../..

# # import
# mkdir -p .cppmake/import
# touch .cppmake/import/g++-mapper.txt
# echo "std .cppmake/import/std.gcm" > .cppmake/import/g++-mapper.txt
# g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/import/g++-mapper.txt -c $(find $(dirname $(which g++))/.. | grep "std.cc" | head -n 1) -o .cppmake/import/std.o
# echo "cppmake .cppmake/import/cppmake.gcm" > .cppmake/import/g++-mapper.txt
# g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/import/g++-mapper.txt -Wno-expose-global-module-tu-local -Iinclude -I.cppmake/pkg/boost/install/include -c import/cppmake.cpp -o .cppmake/import/cppmake.o -fdiagnostics-add-output=sarif:file=.cppmake/import/cppmake.sarif

# lib
mkdir -p .cppmake/lib
g++ -shared .cppmake/import/cppmake.o .cppmake/pkg/boost/install/lib/*.a -o .cppmake/lib/cppmake.so

# # bin
# mkdir -p .cppmake/bin
# g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/import/g++-mapper.txt -c bin/main.cpp -o .cppmake/bin/main.o -fdiagnostics-add-output=sarif:file=.cppmake/bin/main.sarif
# g++ .cppmake/bin/main.o .cppmake/lib/cppmake.so -o .cppmake/bin/main
