set -x

cd pkg/boost/git
./bootstrap.sh --with-bjam=./b2
./b2 --with-process --with-program_options --build-dir=../../../.cppmake/pkg/boost/.build --prefix=../../../.cppmake/pkg/boost link=static install
cd ../../..

mkdir -p .cppmake/pkg/boost/import
echo "boost.asio .cppmake/pkg/boost/import/boost.asio.gcm" >> .cppmake/.mapper
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -I.cppmake/pkg/boost/include -Wno-expose-global-module-tu-local -c pkg/boost/import/boost/asio.cpp -o .cppmake/pkg/boost/import/boost.asio.o
echo "boost.dll .cppmake/pkg/boost/import/boost.dll.gcm" >> .cppmake/.mapper
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -I.cppmake/pkg/boost/include -Wno-expose-global-module-tu-local -c pkg/boost/import/boost/dll.cpp -o .cppmake/pkg/boost/import/boost.dll.o
echo "boost.process .cppmake/pkg/boost/import/boost.process.gcm" >> .cppmake/.mapper
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -I.cppmake/pkg/boost/include -Wno-expose-global-module-tu-local -c pkg/boost/import/boost/process.cpp -o .cppmake/pkg/boost/import/boost.process.o
echo "boost.program_options .cppmake/pkg/boost/import/boost.program_options.gcm" >> .cppmake/.mapper
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -I.cppmake/pkg/boost/include -Wno-expose-global-module-tu-local -c pkg/boost/import/boost/program_options.cpp -o .cppmake/pkg/boost/import/boost.program_options.o
