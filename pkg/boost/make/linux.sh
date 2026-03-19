set -x

cd pkg/boost/git
./bootstrap.sh
./b2 --with-process --with-program_options --build-dir=../../../.cppmake/pkg/boost/build --prefix=../../../.cppmake/pkg/boost/install link=static install
cd ../../..

mkdir -p .cppmake/pkg/boost/install/import
echo "boost.asio    .cppmake/pkg/boost/install/import/boost.asio.gcm"    >> .cppmake/.mapper
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -I.cppmake/pkg/boost/install/include -Wno-expose-global-module-tu-local -c pkg/boost/import/boost/asio.cpp    -o .cppmake/pkg/boost/install/import/boost.asio.o
echo "boost.dll     .cppmake/pkg/boost/install/import/boost.dll.gcm"     >> .cppmake/.mapper
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -I.cppmake/pkg/boost/install/include -Wno-expose-global-module-tu-local -c pkg/boost/import/boost/dll.cpp     -o .cppmake/pkg/boost/install/import/boost.dll.o
echo "boost.process .cppmake/pkg/boost/install/import/boost.process.gcm" >> .cppmake/.mapper
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -I.cppmake/pkg/boost/install/include -Wno-expose-global-module-tu-local -c pkg/boost/import/boost/process.cpp -o .cppmake/pkg/boost/install/import/boost.process.o
echo "boost         .cppmake/pkg/boost/install/import/boost.gcm"         >> .cppmake/.mapper
g++ -std=c++26 -fmodules -fmodule-mapper=.cppmake/.mapper -I.cppmake/pkg/boost/install/include -Wno-expose-global-module-tu-local -c pkg/boost/import/boost.cpp         -o .cppmake/pkg/boost/install/import/boost.o
