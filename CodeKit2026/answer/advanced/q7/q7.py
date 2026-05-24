n = int(input())
arr = list(map(int, input().split()))
if n == 1:
    print(arr[0])
else:
    best = float("-inf")
    for length in range(2, n + 1):
        cur = sum(arr[:length])
        best = max(best, cur)
        for i in range(length, n):
            cur += arr[i] - arr[i - length]
            best = max(best, cur)
    print(best)
