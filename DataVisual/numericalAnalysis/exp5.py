A = [
    [-4, 1, 1, 1],
    [1, -4, 1, 1],
    [1, 1, -4, 1],
    [1, 1, 1, -4]
]
B = [1, 1, 1, 1]
E = 1e-6

def abs(x):
    return x if x>=0 else -x

def GS(n):
    X = n * [0]
    while True:
        e = 0
        for i in range(n):
            y = B[i]
            for j in range(n):
                if j == i:
                    continue
                y -= A[i][j]*X[j]
            y /= A[i][i]
            if abs(X[i] - y) > e:
                e = abs(X[i] - y)
            X[i] = y
        if e < E:
            break
    return X

if __name__ == '__main__':
    X = GS(4)
    print(X)
    X = [round(i, 3) for i in X]
    print(X)