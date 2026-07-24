n = int(input())
arr = list(map(int, input().split()))
ok = all(arr[i] < arr[i + 1] for i in range(n - 1))
print("YES" if ok else "NO")
