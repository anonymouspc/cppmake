# Make packages
(
    cd pkg/boost
    ./bootstrap.sh
    ./b2 --with-process --with-program-options --build-dir=../../.cppmake/pkg/boost/build --prefix=../../.cppmake/pkg/boost/install link=static install
)

# Make cppmake
mkdir -p .cppmake/bin
g++ -std=c++26 -Iinclude -I.cppmake/pkg/boost/install/include bin/cppmake.cpp -o .cppmake/bin/cppmake
