# Make packages
mkdir -p .cppmake/pkg
pkg/boost/bootstrap.sh
pkg/boost/b2 --with-asio --with-process link=static --build-dir=.cppmake/pkg/boost/build --prefix=.cppmake/pkg/boost/install 

# Make cppmake
mkdir -p .cppmake/bin
clang++ -std=c++26 -I.cppmake/pkg/boost/install/include bin/cppmake.cpp -o .cppmake/bin/cppmake