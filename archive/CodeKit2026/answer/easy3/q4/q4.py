n = int(input())
arr = list(map(int, input().split()))
from collections import Counter

cnt = Counter(arr)
best_freq = max(cnt.values())
print(min(x for x, f in cnt.items() if f == best_freq))
