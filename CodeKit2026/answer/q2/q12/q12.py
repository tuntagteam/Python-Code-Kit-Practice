n, k = map(int, input().split())
arr = list(map(int, input().split()))
found = False
for i in range(n):
    for j in range(i + 1, n):
        if arr[i] + arr[j] == k:
            found = True
            break
    if found:
        break
print("YES" if found else "NO")
