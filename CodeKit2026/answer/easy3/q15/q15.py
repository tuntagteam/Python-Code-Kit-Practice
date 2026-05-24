n = int(input())
arr = list(map(int, input().split()))
from collections import Counter

cnt = Counter(arr)
print(sum((v // 2) * 2 for v in cnt.values()))
