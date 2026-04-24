import math

n, m = map(int, input().split())

steps = (n - 1) + (m - 1)
down = n - 1

print(math.comb(steps, down))