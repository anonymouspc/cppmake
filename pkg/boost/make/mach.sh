set -x

cd pkg/boost/git
./bootstrap.sh
./b2 --with-process --with-program_options --build-dir=../../../.cppmake/pkg/boost/.build --prefix=../../../.cppmake/pkg/boost link=static install
cd ../../..

mkdir -p .cppmake/pkg/boost/import
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/pkg/boost/import -I.cppmake/pkg/boost/include --precompile -x c++-module pkg/boost/import/boost/asio.cpp -o .cppmake/pkg/boost/import/boost.asio.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/pkg/boost/import/boost.asio.pcm -o .cppmake/pkg/boost/import/boost.asio.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/pkg/boost/import -I.cppmake/pkg/boost/include --precompile -x c++-module pkg/boost/import/boost/dll.cpp -o .cppmake/pkg/boost/import/boost.dll.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/pkg/boost/import/boost.dll.pcm -o .cppmake/pkg/boost/import/boost.dll.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/pkg/boost/import -I.cppmake/pkg/boost/include --precompile -x c++-module pkg/boost/import/boost/process.cpp -o .cppmake/pkg/boost/import/boost.process.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/pkg/boost/import/boost.process.pcm -o .cppmake/pkg/boost/import/boost.process.o
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/pkg/boost/import -I.cppmake/pkg/boost/include --precompile -x c++-module pkg/boost/import/boost.cpp -o .cppmake/pkg/boost/import/boost.pcm
clang++ -std=c++26 -fprebuilt-module-path=.cppmake/pkg/boost/import -c .cppmake/pkg/boost/import/boost.pcm -o .cppmake/pkg/boost/import/boost.o
