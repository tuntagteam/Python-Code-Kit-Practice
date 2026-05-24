MOD = 10**9 + 7
n, x = map(int, input().split())
coeffs = list(map(int, input().split()))
result = 0
for a in coeffs:
    result = (result * x + a) % MOD
print(result)
