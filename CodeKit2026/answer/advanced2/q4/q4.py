from collections import deque

n, k = map(int, input().split())
arr = list(map(int, input().split()))
dq = deque()
result = []
for i, val in enumerate(arr):
    while dq and arr[dq[-1]] <= val:
        dq.pop()
    dq.append(i)
    if dq[0] <= i - k:
        dq.popleft()
    if i >= k - 1:
        result.append(arr[dq[0]])
print(*result)
