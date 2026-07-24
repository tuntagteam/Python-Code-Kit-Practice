s = input().strip()
found = any(s[i] == s[i + 1] for i in range(len(s) - 1))
print("YES" if found else "NO")
