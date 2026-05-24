from collections import deque

r, c = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(r)]
visited = [[False] * c for _ in range(r)]
best = 0

for i in range(r):
    for j in range(c):
        if grid[i][j] == 1 and not visited[i][j]:
            size = 0
            queue = deque([(i, j)])
            visited[i][j] = True
            while queue:
                x, y = queue.popleft()
                size += 1
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < r and 0 <= ny < c and grid[nx][ny] == 1 and not visited[nx][ny]:
                        visited[nx][ny] = True
                        queue.append((nx, ny))
            best = max(best, size)
print(best)
