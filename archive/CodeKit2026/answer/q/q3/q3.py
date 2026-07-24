n = int(input())
arr = list(map(int, input().split()))
ok = all(arr[i] <= arr[i + 1] for i in range(n - 1))
print("SORTED" if ok else "UNSORTED")
