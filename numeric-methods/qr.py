import numpy as np

def main():
    A  = np.array(((
    (3, 4),
    (4, 0)
    )))

    #A = np.abs(np.floor(np.random.randn(10, 10)*10))

    Q, R = qr(A)
    print(Q.round(2))
    print(R.round(2))
    print((Q@R).round(2))


def qr(A):
    rows, cols = A.shape
    Q = np.eye(rows)
    for i in range(cols - (rows == cols)):
        H = np.eye(rows)
        H[i:, i:] = get_householder(A[i:, i])
        Q = np.dot(Q, H)
        A = np.dot(H, A)
    return Q, A

def get_householder(a):
    H = np.eye(a.shape[0])
    norm = np.linalg.norm
    if norm(a) == 0 or a == []:
        return H
    v = a/(a[0] + np.copysign(norm(a), a[0]))
    v[0] = 1
    print(v)
    H -= (2/np.dot(v, v))*np.outer(v, v)

    return H


if __name__ == '__main__':
    main()
