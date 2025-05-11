def num_islands(grid, m, n):
    count = 0
    def bfs(i, j):
        queue = [(i, j)]
        grid[i][j] = '0'  
        while queue:
            x, y = queue.pop(0)
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == '1':
                    grid[nx][ny] = '0'
                    queue.append((nx, ny))

    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                count += 1
                bfs(i, j)
    return count

m, n = map(int, input().split())
grid = [list(input().strip()) for _ in range(m)]

print(num_islands(grid, m, n))