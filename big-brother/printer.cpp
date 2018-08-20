#include <iostream>
#include <chrono>
#include <thread>
#include <string>
#include <stdlib.h>    // system, NULL, EXIT_FAILURE

int main(int argc, char const *argv[])
{
	//std::string command("pstree -p " + argv[1] + " > proccess.txt");
	system("pstree -p 1 > proccess.txt");
}