n = int(input())
arr = list(map(int, input().split()))
if n < 3:
    print(0)
else:
    up = [1] * n
    down = [1] * n
    for i in range(1, n):
        if arr[i] > arr[i - 1]:
            up[i] = up[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if arr[i] > arr[i + 1]:
            down[i] = down[i + 1] + 1
    best = 0
    for i in range(1, n - 1):
        if up[i] > 1 and down[i] > 1:
            best = max(best, up[i] + down[i] - 1)
    print(best)
