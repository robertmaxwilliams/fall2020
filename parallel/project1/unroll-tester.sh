#!/bin/sh
g++ -Wno-c++11-extensions -O0 unroll.cpp -o unroll-0.out
echo "Three runs of 0"
./unroll-0.out
./unroll-0.out
./unroll-0.out
g++ -Wno-c++11-extensions -O1 unroll.cpp -o unroll-1.out
echo "Three runs of 1"
./unroll-1.out
./unroll-1.out
./unroll-1.out
g++ -Wno-c++11-extensions -O2 unroll.cpp -o unroll-2.out
echo "Three runs of 2"
./unroll-2.out
./unroll-2.out
./unroll-2.out
g++ -Wno-c++11-extensions -O3 unroll.cpp -o unroll-3.out
echo "Three runs of 3"
./unroll-3.out
./unroll-3.out
./unroll-3.out
g++ -Wno-c++11-extensions -Ofast unroll.cpp -o unroll-fast.out
echo "Three runs of fast"
./unroll-fast.out
./unroll-fast.out
./unroll-fast.out
