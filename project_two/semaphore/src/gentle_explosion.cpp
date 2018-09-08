/**
 * @file    gentle_explosion.cpp
 * @brief   Driver code to test Beagle Bone's GPIO
 * @author  Lucas Gomes Dantas (dantaslucas@ufrn.edu.br)
 * @author  Lucas Aléssio Anunciado Silva (lucas.alessio@live.com)
 * @date    September 4h, 2018
 */

#include <algorithm>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>


/**
 * @brief      This function will simply stress out the memory usage of the
 *             Beagle Bone Board (BBB). We tried to perform actions that do
 *             require a lot of processing without completely crashing the
 *             board. All values here used were decided through empirical
 *             analisys and may not be sufficient to stress out your own BBB.
 *
 * @param[in]  argc  The argc
 * @param      argv  The argv
 *
 * @return     Nothing
 */
int main(int argc, char const *argv[])
{
	std::vector<int> explosion;
	explosion.resize(1000000);

	// Here the memory usage will increase, but still only green LED will be turned on
	std::iota(explosion.begin(), explosion.end(), 1);
	std::shuffle(explosion.begin(), explosion.end(), std::mt19937{std::random_device{}()});

	// The memory will increase exponentially, turning on the other LEDs
	explosion.resize(90111111);
	std::iota(explosion.begin(), explosion.end(), 1);
	std::shuffle(explosion.begin(), explosion.end(), std::mt19937{std::random_device{}()});
}