def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


a, m = map(int, input().split())
g, x, _ = extended_gcd(a, m)
if g != 1:
    print(-1)
else:
    print(x % m)
