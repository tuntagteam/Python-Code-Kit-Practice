from collections import Counter

s = input().strip()
t = input().strip()
need = Counter(t)
required = len(t)
left = 0
formed = 0
window = Counter()
best_len = float("inf")
best_start = 0

for right, ch in enumerate(s):
    window[ch] += 1
    if ch in need and window[ch] == need[ch]:
        formed += 1
    while formed == required:
        if right - left + 1 < best_len:
            best_len = right - left + 1
            best_start = left
        left_ch = s[left]
        window[left_ch] -= 1
        if left_ch in need and window[left_ch] < need[left_ch]:
            formed -= 1
        left += 1

print("" if best_len == float("inf") else s[best_start : best_start + best_len])
