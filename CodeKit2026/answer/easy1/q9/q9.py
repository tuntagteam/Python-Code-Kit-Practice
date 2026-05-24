n, k = map(int, input().split())
arr = list(map(int, input().split()))
seen = set()
found = False
for x in arr:
    if k - x in seen:
        found = True
        break
    seen.add(x)
print("YES" if found else "NO")
