import std;
import cppmake;

int main ( )
{
    std::println("{}", (std::stringstream() << cppmake::config.compile_std).str());
    std::println("{}", cppmake::config.verbose);
}