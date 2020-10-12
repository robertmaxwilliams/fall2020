#define N 1000
#include <time.h>
#include <stdlib.h>
#include <stdio.h>

// `matmul_macro` allows for the loop variables i, j, k to be
// put in any order with a single macro call
#define matmul_macro(name, var1, var2, var3)\
void (name)(float* A, float* B, float* C) {\
    for (int var1 = 0; var1 < N; var1++) {\
        for (int var2 = 0; var2 < N; var2++) {\
            for (int var3 = 0; var3 < N; var3++) {\
                 C[i+j*N] += A[i+k*N] * B[k+j*N]; \
            }\
        }\
    }\
}

// This defines all six functions using the above macro
matmul_macro(matmul1, i, j, k);
matmul_macro(matmul2, i, k, j);
matmul_macro(matmul3, k, i, j);
matmul_macro(matmul4, j, i, k);
matmul_macro(matmul5, k, j, i);
matmul_macro(matmul6, j, k, i);

// TIME takes a function name and calls it on A, B, C and times how long it takes,
// printing the result
#define TIME(name)\
t = clock();\
(name)(A, B, C);\
printf("The output is %f\n", C[0]);\
t = clock() - t;\
printf (#name " took me %lu clicks (%.3f seconds).\n", t, ((float)t)/(CLOCKS_PER_SEC));


// Sets the elements of an array to random numbers 0.00 to .99 by increments of .01
float* initialize(float* arr) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            arr[i+j*N] = (rand() % 100) / 100.0;
        }
    }
    return arr;
}

int main() {
    float* A = initialize(malloc(sizeof(float) * N * N));
    float* B = initialize(malloc(sizeof(float) * N * N));
    float* C = malloc(sizeof(float) * N * N);
    printf ("Done allocating\n");
    srand(time(NULL));
    clock_t t;
    TIME(matmul1);
    TIME(matmul2);
    TIME(matmul3);
    TIME(matmul4);
    TIME(matmul5);
    TIME(matmul6);
    return 0;
}
