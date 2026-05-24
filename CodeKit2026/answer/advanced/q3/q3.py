from collections import deque

n, m = map(int, input().split())
graph = [[] for _ in range(n + 1)]
for _ in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

start, goal = map(int, input().split())
visited = {start}
queue = deque([start])
while queue:
    node = queue.popleft()
    if node == goal:
        print("YES")
        break
    for nxt in graph[node]:
        if nxt not in visited:
            visited.add(nxt)
            queue.append(nxt)
else:
    print("NO")
