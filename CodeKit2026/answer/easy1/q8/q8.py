n = int(input())
arr = list(map(int, input().split()))
cur = best = arr[0]
for i in range(1, n):
    cur = max(arr[i], cur + arr[i])
    best = max(best, cur)
print(best)
