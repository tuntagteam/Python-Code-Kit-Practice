s = "abcabcbb"
start = 0
seen = {}
max_len = 0
for end in range(len(s)):
    if s[end] in seen and seen[s[end]] >= start:
        start = seen[s[end]] + 1
    seen[s[end]] = end
    max_len = max(max_len, end - start + 1)
print("Longest unique substring length:", max_len)