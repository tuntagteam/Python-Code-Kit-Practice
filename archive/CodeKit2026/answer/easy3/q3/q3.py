n = int(input())
arr = list(map(int, input().split()))
from collections import Counter

cnt = Counter(arr)
for x in arr:
    if cnt[x] == 1:
        print(x)
        break
