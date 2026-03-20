import std;
import cppmake;

int main ( )
{
    std::println("{}", cppmake::resolve(cppmake::resolvable_path("g++-15")).c_str());
}