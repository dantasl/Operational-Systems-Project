#include <iostream>
#include <chrono>
#include <thread>
#include <stdlib.h>    // system, NULL, EXIT_FAILURE

int main ()
{
	using namespace std::this_thread; // sleep_for, sleep_until
    using namespace std::chrono; // nanoseconds, system_clock, seconds

	std::cout << "Big Brother is now watching your processes." << std::endl;
	while(true)
	{
		//std::cout << std::endl << "Number of processes running right now: ";
		system("ps aux | wc -l");
		//sleep_until(system_clock::now() + seconds(1));
		//std::cout << "Number of processes running classified by user: ";
		system("ps -eo user=|sort|uniq -c");
    	sleep_until(system_clock::now() + seconds(3)); // waits 3 seconds before show processes again
	}	
	std::cout << std::endl << "Big Brother now rests." << std::endl;
}