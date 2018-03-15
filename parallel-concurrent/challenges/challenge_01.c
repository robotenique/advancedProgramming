#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 80000000

// Counts which elements of v are greater than N/2 and which aren't
void checkNumbers(int *v){
    int k;
    int a = 0, b = 0;
    k = 0;
    while (k < N) {
        if(v[k] > N/2)
            a++;
        else
            b++;
        k++;
    }
}

int main(int argc, char const *argv[]) {
    srand(time(NULL));

    int *v = malloc(N*sizeof(int));
    for (int i = 0; i < N; i++)
        v[i] = i + 1;

    printf("50 first numbers: \n");
    for (int i = 0; i < (int)(N > 100 ? 50 : 0.2*N); i++)
        printf("%d, ", v[i]);

    // Time of the first method
    clock_t t;
    t = clock();
    checkNumbers(v);
    t = clock() - t;
    double time_taken = 100*((double)t)/CLOCKS_PER_SEC;
    printf("\ntime of the first = %fms\n\n", time_taken);

    // Fisher-yates shuffle
    int temp;
    for (int i = 0; i < N; i++) {
        int r = (int) rand()%(i + 1);
        temp = v[r];
        v[r] = v[i];
        v[i] = temp;
    }

    printf("50 first numbers: \n");
    for (int i = 0; i < (int)(N > 100 ? 50 : 0.2*N); i++)
        printf("%d, ", v[i]);


    // Time of of the second method
    t = clock();
    checkNumbers(v);
    t = clock() - t;
    time_taken = 100*((double)t)/CLOCKS_PER_SEC;
    printf("\ntime of the second = %fms\n", time_taken);

    return 0;
}
