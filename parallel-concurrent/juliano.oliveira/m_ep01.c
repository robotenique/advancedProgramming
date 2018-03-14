#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define N 15000

// TODO: Comment what this does

void printMatrix(int **m){
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++)
      printf("%03d ", m[i][j]);
    printf("\n");
  }
}


void countMatrix_1(int **m){
    int counter = 0;
    int garbage = 0;
    for (int i = 0; i < N; i++)
      for (int j = 0; j < N; j++){
        garbage += m[i][j] % 10;
        garbage %= 100;
        counter++;
    }
    printf("Finish optimizedCount");
}

void countMatrix_2(int **m){
    int counter = 0;
    int garbage = 0;
    for (int i = 0; i < N; i++)
      for (int j = 0; j < N; j++){
        garbage += m[j][i]  % 10;
        garbage %= 100;
        counter++;
    }
	printf("Finish unoptimizedCount");
}


int main(int argc, char const *argv[]) {
    srand(time(NULL));
    int ** mA = malloc(N*sizeof(int*));
    for (int i = 0; i < N; i++)
    mA[i] = malloc(N*sizeof(int));
    for (int i = 0; i < N; i++)
    	for (int j = 0; j < N; j++)
    		mA[i][j] = rand()%((long)N*N);

    printf("\n ======== Test with %d x %d matrix =======\n", N, N);
    // Time of the first method
    clock_t t;
    t = clock();
    countMatrix_1(mA);
    t = clock() - t;
    double time_taken = 100*((double)t)/CLOCKS_PER_SEC;
    double t1 = time_taken;
    printf(" time = %fms\n", time_taken);

    // Time of of the second method
    t = clock();
    countMatrix_2(mA);
    t = clock() - t;
    time_taken = 100*((double)t)/CLOCKS_PER_SEC;
    double t2 = time_taken;
    printf(" time = %fms\n", time_taken);

    printf("Razão (optimized/unoptimized) = %lf\n", t1/t2);
  return 0;
}
