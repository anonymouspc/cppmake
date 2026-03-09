mkdir -p .cppmake
clang++ -std=c++26 -Ipkg/boost/asio/include bin/cppmake.cpp -o .cppmake/bin/cppmake