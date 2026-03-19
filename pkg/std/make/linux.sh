set -x

mkdir -p .cppmake/pkg/std/install/import
echo "std .cppmake/pkg/std/install/import/std.gcm" >> .cppmake/.mapper
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -fsearch-include-path -c bits/std.cc -o .cppmake/import/std.o
