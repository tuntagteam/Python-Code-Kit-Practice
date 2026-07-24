import math

a, b = map(int, input().split())

answer = a * b // math.gcd(a, b)

print(answer)