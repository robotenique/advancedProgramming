#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// TODO: Comment and organize
#define N 80000000

int main(int argc, char const *argv[]) {
    srand(time(NULL));

    int *v = malloc(N*sizeof(int));
    for (int i = 0; i < N; i++)
        v[i] = i + 1;
    int k;
    int a = 0, b = 0;

    for (int i = 0; i < (int)(N > 100 ? 50 : 0.2*N); i++)
        printf("%d, ", v[i]);
    printf("\n\n");
    // Time of the first method
    clock_t t;
    t = clock();

    k = 0;
    while (k < N) {
        if(v[k] > N/2)
            a++;
        else
            b++;
        k++;
    }

    t = clock() - t;
    double time_taken = 100*((double)t)/CLOCKS_PER_SEC;
    printf(" time = %fms\n", time_taken);


    int temp;
    for (int i = 0; i < N; i++) {
        int r = (int) rand()%(i + 1);
        temp = v[r];
        v[r] = v[i];
        v[i] = temp;
    }

    for (int i = 0; i < (int)(N > 100 ? 50 : 0.2*N); i++)
        printf("%d, ", v[i]);
    printf("\n\n");

    // Time of of the second method
    t = clock();
    k = 0;
    while (k < N) {
        if(v[k] > N/2)
            a++;
        else
            b++;
        k++;
    }
    t = clock() - t;
    time_taken = 100*((double)t)/CLOCKS_PER_SEC;
    printf(" time = %fms\n", time_taken);




    return 0;
}
