/*
 *
 *
 */

#include <algorithm>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>

int main(int argc, char const *argv[])
{
	std::vector<int> explosion;
	explosion.resize(1000000);

	// Here the memory usage will increase, but still only green LED
	std::iota(explosion.begin(), explosion.end(), 1);
	std::shuffle(explosion.begin(), explosion.end(), std::mt19937{std::random_device{}()});

	// The memory will increase exponentially, turning on the other LEDs
	explosion.resize(90111111);
	std::iota(explosion.begin(), explosion.end(), 1);
	std::shuffle(explosion.begin(), explosion.end(), std::mt19937{std::random_device{}()});
}