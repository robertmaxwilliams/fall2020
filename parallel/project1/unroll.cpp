#include "chrono_timer.h"
#include <cstdint> // define uint64_t, etc.
#include <random>


// https://stackoverflow.com/a/36527160/8571734
float get_random()
{
    static std::default_random_engine e;
    static std::uniform_real_distribution<> dis(0, 1); // range 0 - 1
    return dis(e);
}

float plain_max(float * data, uint64_t length)
{
    float max = -INFINITY;
    for (uint64_t i = 0; i < length; i++)
        max = std::max(max, data[i]);
    return max;
}

float plain_max_unroll_2(float * data, uint64_t length)
{
    float max_0 = -INFINITY;
    float max_1 = -INFINITY;
    for (uint64_t i = 0; i < length; i += 2)
    {
        max_0 = std::max(max_0, data[i+0]);
        max_1 = std::max(max_1, data[i+1]);
    }
    return std::max(max_0, max_1);
}

float plain_max_unroll_4(float * data, uint64_t length)
{
    float max_0 = -INFINITY;
    float max_1 = -INFINITY;
    float max_2 = -INFINITY;
    float max_3 = -INFINITY;
    for (uint64_t i = 0; i < length; i += 4)
    {
        max_0 = std::max(max_0, data[i+0]);
        max_1 = std::max(max_1, data[i+1]);
        max_2 = std::max(max_2, data[i+2]);
        max_3 = std::max(max_3, data[i+3]);
    }
    return std::max(max_0, std::max(max_1,
                std::max(max_2, max_3)));
}

#define MANY 268435456
int main() {

    unsigned seed = 42;
    std::default_random_engine generator (seed);
    std::uniform_real_distribution<double> distribution (0.0,100.0);

    float* data;
    data = (float*) malloc(sizeof(float) * MANY);
    for (int i = 0; i < MANY; i++)
            data[i] = distribution(generator);
    INIT_TIMER;




    START_TIMER;
    float a = plain_max(data, MANY);
    STOP_TIMER("plain");

    START_TIMER;
    float b = plain_max_unroll_2(data, MANY);
    STOP_TIMER("two");

    START_TIMER;
    float c = plain_max_unroll_4(data, MANY);
    STOP_TIMER("four");

    printf("%f %f %f\n", a, b, c);
    return 0;
}
