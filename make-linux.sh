set -x

mkdir -p .cppmake/import
truncate -s 0 .cppmake/.mapper

./pkg/std/make/linux.sh
./pkg/boost/make/linux.sh
./make/linux.sh
