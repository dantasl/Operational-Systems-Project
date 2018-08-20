#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <string>
#include <iterator>
#include <vector>

std::vector<std::string> get_info (const char* pid, std::vector<std::string> arguments)
{
    std::ifstream status;
    std::string line;
    std::vector<std::string> info;
    status.open ("/proc/" + std::string(pid) + "/status" );
    while (std::getline(status, line))
    {
        for ( auto it(arguments.begin()); it != arguments.end(); ++it )
        {
            auto size ( std::string(*it).length() );
            if ( (line.substr(0, size)).compare(*it) == 0 )
            {
                info.push_back (line);
                break;
            }
        }
    }
    return info;
}

void print_result (std::vector<std::string> result)
{
    for ( auto it(result.begin()); it != result.end(); ++it )
        std::cout << *it << std::endl;
}

int main (int const argc, char const **argv)
{
    if (argc != 2)
    {
        std::cout << "Invalid arguments." << std::endl;
        exit (EXIT_FAILURE);
    }

    std::vector<std::string> arguments = { "Name", "State", "voluntary_ctxt_switches", "nonvoluntary_ctxt_switches" };

    print_result(get_info (argv[1], arguments));
}