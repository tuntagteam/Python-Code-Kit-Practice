n, k = map(int, input().split())
arr = list(map(int, input().split()))
window = sum(arr[:k])
best = window
for i in range(k, n):
    window += arr[i] - arr[i - k]
    best = max(best, window)
print(best)
