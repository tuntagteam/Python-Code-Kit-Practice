s = input().strip()
from collections import Counter

cnt = Counter(s)
best = max(cnt.values())
for ch in sorted(cnt):
    if cnt[ch] == best:
        print(ch, cnt[ch])
        break
