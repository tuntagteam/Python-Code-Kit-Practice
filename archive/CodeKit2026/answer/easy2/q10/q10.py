n = int(input())
arr = list(map(int, input().split()))
if n == 1:
    print(arr[0])
else:
    prev2, prev1 = arr[0], max(arr[0], arr[1])
    for i in range(2, n):
        cur = max(prev1, prev2 + arr[i])
        prev2, prev1 = prev1, cur
    print(prev1)
