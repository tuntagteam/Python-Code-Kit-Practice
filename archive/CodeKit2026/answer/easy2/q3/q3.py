n = int(input())
arr = list(map(int, input().split()))
from collections import Counter

cnt = Counter(arr)
ans = -1
for x in arr:
    if cnt[x] == 1:
        ans = x
        break
print(ans)
