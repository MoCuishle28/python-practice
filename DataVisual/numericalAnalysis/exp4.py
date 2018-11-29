A = [
    [10, -7, 0, 1],
    [-3, 2.099999, 6, 2],
    [5, -1, 5, -1],
    [2, 1, 0, 2]
]
B = [8, 5.900001, 5, 1]

def uni():
    C = A
    for i in zip(C, B):
        i[0].append(i[1])
    return C


def solve():
    det = 1
    for k in range(len(A) - 1):
        ik = k
        for i in range(k + 1, len(A)):
            if A[ik][k] < A[i][k]:
                ik = i
        if A[ik][k] < 1e-6:
            det = 0
            break
        if ik != k:
            for j in range(k, len(A[0])):
                A[k][j], A[ik][j] = A[ik][j], A[k][j]
            det = -det
        for i in range(k + 1, len(A)):
            A[i][k] /= A[k][k]
            for j in range(k + 1, len(A[0])):
                A[i][j] -= A[i][k]*A[k][j]
        det *= A[k][k]
    n = len(A) - 1
    if A[n][n] < 1e-6:
        det = 0
        return det
    else:
        A[n][n + 1] /= A[n][n]
        for i in range(n-1, -1, -1):
            for j in range(i + 1, len(A)):
                A[i][n + 1] -= A[i][j] * A[j][n+1]
            A[i][n + 1] /= A[i][i]
    det *= A[n][n]
    return det

def fabs(x):
    return x if x >= 0 else -x

if __name__ == '__main__':

    A = uni()
    det = solve()
    x = []
    for i in A:
        t = i.pop()
        x.append((0 if fabs(t) < 1e-6 else round(t, 6)))
    print("\ndet = %.2f" %(det), "\nX = ", x)
