"""Implements Cholesky Matrix Factorization A = LL.T, if A is a positive defined matrix
"""
import numpy as np

def main():
    # Matrix example
    A = np.array([[1, 1, 3],
                  [1, 5, 5],
                  [3, 5, 19]], dtype=float)
    L = cholesky(A)
    print(f"L = \n {L}")
    print(f"L@L.T = \n{L@L.T}")
    print(f"A = \n{A}")

def cholesky(A):
    L = A.copy()
    for i in range(len(L)):
        L[i, i] = np.sqrt(L[i, i])
        L[i+1:, i] /= L[i, i]
        L[i, i+1:] *= 0
        L[i+1:, i+1:] -= np.outer(L[i+1:, i], L[i+1:, i])
    return L

if __name__ == '__main__':
    main()