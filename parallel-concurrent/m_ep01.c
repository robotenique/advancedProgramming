#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define N 25000


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
    printf("Finish countMatrix_1");
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
	printf("Finish countMatrix_2");
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
    printf(" time = %fms\n", time_taken);

    // Time of of the second method
    t = clock();
    countMatrix_2(mA);
    t = clock() - t;
    time_taken = 100*((double)t)/CLOCKS_PER_SEC;
    printf(" time = %fms\n", time_taken);

  return 0;
}
