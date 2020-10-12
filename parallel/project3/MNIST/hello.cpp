#include <iostream>
#include <cstdint>
#include <vector>
#include <thread>
void say_hello(uint64_t id)
{
    std::cout << "Hello from thread: " << id << std::endl;
}
int main()
{
    const uint64_t num_threads = 6;
    std::vector<std::thread> threads;

    for (uint64_t id = 0; id < num_threads; id++) {
        threads.emplace_back(say_hello, id);
    }
    for (auto& thread: threads)
        thread.join();
}
