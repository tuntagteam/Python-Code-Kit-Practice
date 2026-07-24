n, k = map(int, input().split())
arr = list(map(int, input().split()))
best = float("-inf")
for i in range(n - k + 1):
    seg = arr[i : i + k]
    best = max(best, max(seg) - min(seg))
print(best)
