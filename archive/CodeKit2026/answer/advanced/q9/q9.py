n = int(input())
arr = list(map(int, input().split()))
total = sum(arr)
target = total // 2
dp = [False] * (target + 1)
dp[0] = True
for x in arr:
    for j in range(target, x - 1, -1):
        dp[j] = dp[j] or dp[j - x]
best = 0
for j in range(target, -1, -1):
    if dp[j]:
        best = j
        break
print(total - 2 * best)
