import heapq

n, m, k = map(int, input().split())
graph = [[] for _ in range(n)]
for _ in range(m):
    a, b, w = map(int, input().split())
    graph[a].append((b, w))
    graph[b].append((a, w))
packages = list(map(int, input().split()))

nodes = [0] + packages
idx = {node: i for i, node in enumerate(nodes)}
size = len(nodes)
dist = [[float("inf")] * n for _ in range(size)]

for i, src in enumerate(nodes):
    d = [float("inf")] * n
    d[src] = 0
    pq = [(0, src)]
    while pq:
        cost, u = heapq.heappop(pq)
        if cost > d[u]:
            continue
        for v, w in graph[u]:
            nd = cost + w
            if nd < d[v]:
                d[v] = nd
                heapq.heappush(pq, (nd, v))
    for j, dst in enumerate(nodes):
        dist[i][j] = d[dst]

full = (1 << k) - 1
dp = [[float("inf")] * size for _ in range(1 << k)]
dp[0][0] = 0

for mask in range(1 << k):
    for last in range(size):
        cur = dp[mask][last]
        if cur == float("inf"):
            continue
        for nxt in range(1, size):
            bit = 1 << (nxt - 1)
            if mask & bit:
                continue
            new_mask = mask | bit
            nd = cur + dist[last][nxt]
            if nd < dp[new_mask][nxt]:
                dp[new_mask][nxt] = nd

print(min(dp[full][i] for i in range(1, size)))
