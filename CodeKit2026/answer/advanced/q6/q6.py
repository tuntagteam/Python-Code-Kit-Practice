n, k = map(int, input().split())
arr = list(map(int, input().split()))
seen = {}
count = 0
for x in arr:
    if k - x in seen:
        count += seen[k - x]
    seen[x] = seen.get(x, 0) + 1
print(count)
