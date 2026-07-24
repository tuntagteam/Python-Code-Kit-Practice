MOD = 10**9 + 7


def mat_mul(a, b):
    return [
        [(a[0][0] * b[0][0] + a[0][1] * b[1][0]) % MOD, (a[0][0] * b[0][1] + a[0][1] * b[1][1]) % MOD],
        [(a[1][0] * b[0][0] + a[1][1] * b[1][0]) % MOD, (a[1][0] * b[0][1] + a[1][1] * b[1][1]) % MOD],
    ]


def mat_pow(mat, power):
    result = [[1, 0], [0, 1]]
    while power:
        if power & 1:
            result = mat_mul(result, mat)
        mat = mat_mul(mat, mat)
        power //= 2
    return result


n = int(input())
if n == 0:
    print(0)
else:
    base = [[1, 1], [1, 0]]
    res = mat_pow(base, n)
    print(res[0][1])
