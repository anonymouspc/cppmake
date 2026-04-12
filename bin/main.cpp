import std;
import cppmake;

int main ( )
{
    std::println("{}", std::type_index(typeid(cppmake::system)) == std::type_index(typeid(cppmake::mach)));
}