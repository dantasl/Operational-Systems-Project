#include <algorithm>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>

int main(int argc, char const *argv[])
{
	std::vector<int> explosion;
	explosion.resize(1000000);

	// Section to stay with green led turned on
	std::iota(explosion.begin(), explosion.end(), 1);
	std::shuffle(explosion.begin(), explosion.end(), std::mt19937{std::random_device{}()});

	// Yellow and red leds get turned on
	explosion.resize(90111111);
	std::iota(explosion.begin(), explosion.end(), 1);
	std::shuffle(explosion.begin(), explosion.end(), std::mt19937{std::random_device{}()});
}