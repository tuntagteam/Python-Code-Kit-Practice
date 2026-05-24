n, k, x = map(int, input().split())
arr = list(map(int, input().split()))
window = sum(arr[:k])
count = 1 if window > x else 0
for i in range(k, n):
    window += arr[i] - arr[i - k]
    if window > x:
        count += 1
print(count)
