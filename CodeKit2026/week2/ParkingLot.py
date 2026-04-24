n = int(input())
a = list(map(int, input().split()))

current = a[0]
best = a[0]

for i in range(1, n):
    current = max(a[i], current + a[i])
    best = max(best, current)

print(best)