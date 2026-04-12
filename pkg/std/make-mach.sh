set -x

mkdir -p .cppmake/pkg/std/import
clang++ -std=c++26 -Wno-reserved-module-identifier --precompile $(clang++ --print-resource-dir)/../../../share/libc++/v1/std.cppm -o .cppmake/pkg/std/import/std.pcm
clang++ -std=c++26 -c .cppmake/pkg/std/import/std.pcm -o .cppmake/pkg/std/import/std.o
