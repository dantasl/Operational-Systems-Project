/**
 * @file    status.cpp
 * @brief   Receives a PID and prompts the arguments selected by the user.
 * @author  Lucas Gomes Dantas (dantaslucas@ufrn.edu.br)
 * @date    August 20th - 2018
 */

#include <iostream> // std::cout, std::endl, etc
#include <fstream> // ifstream and file.open()
#include <stdlib.h> // exit() and EXIT_FAILURE
#include <string> // String manipulation
#include <iterator> // Iterator manipulation
#include <vector> // std::vector

/**
 * @brief   This function will receive a PID and a list of arguments containing what the user
 *          wants to know about the process by its status. It will read the /proc/pid/status
 *          and will add to a vector only the lines that match what the user wants.
 *
 * @param[in]   pid         The process ID to read the status
 * @param[in]   arguments   Reference to vector containing the items that the user wants to know
 *                          about the process.
 * @return      The data found inside status.
 */
std::vector<std::string> get_info (const char* pid, const std::vector<std::string> &arguments)
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

/**
 * @brief   This function will receive a vector containing the information to be printed on screen.
 *
 * @param[in]   result      Vector containing all information to print
 */
void print_result (std::vector<std::string> result)
{
    for ( auto it(result.begin()); it != result.end(); ++it )
        std::cout << *it << std::endl;
}

int main (int const argc, char const **argv)
{
    // It must have exactly two arguments: the name of the program and the PID
    if (argc != 2)
    {
        std::cout << "Invalid arguments." << std::endl;
        exit (EXIT_FAILURE);
    }

    // This can be changed to whatever arguments you want to retrieve from /proc/pid/status
    std::vector<std::string> arguments = { "Name", "State", "voluntary_ctxt_switches", "nonvoluntary_ctxt_switches" };

    print_result(get_info (argv[1], arguments));
}