n = int(input())
arr = list(map(int, input().split()))
best = cur = 0
for x in arr:
    if x > 0:
        cur += 1
        best = max(best, cur)
    else:
        cur = 0
print(best)
