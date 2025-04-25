from collections import deque

maze = [
    list("S.#......."),
    list(".........."),
    list("..*.#....."),
    list("###......."),
    list("...#C.....")
]

n = len(maze)
visited = [[False]*n for _ in range(n)]
parent = [[None]*n for _ in range(n)]

# หาตำแหน่ง S และ C
start = end = None
for i in range(n):
    for j in range(n):
        if maze[i][j] == "S":
            start = (i, j)
        elif maze[i][j] == "C":
            end = (i, j)

def bfs(start, end):
    q = deque()
    q.append((start[0], start[1], 0))  # (x, y, steps)
    visited[start[0]][start[1]] = True

    while q:
        x, y, step = q.popleft()
        if (x, y) == end:
            return step

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                if not visited[nx][ny] and maze[nx][ny] != "#" and maze[nx][ny] != "*":
                    visited[nx][ny] = True
                    parent[nx][ny] = (x, y)
                    q.append((nx, ny, step + 1))
    return -1

result = bfs(start, end)

if result == -1:
    print("ส่งอาหารไม่สำเร็จ")
else:
    print(f"สามารถส่งอาหารได้ใน {result} ก้าว")

    # ✅ ย้อนทางจาก C -> S แล้ว mark จุดเดินด้วย 'P'
    path = []
    x, y = end
    while (x, y) != start:
        path.append((x, y))
        x, y = parent[x][y]
    path.pop()  # ไม่ mark จุด C หรือ S

    for x, y in path:
        if maze[x][y] not in ("S", "C"):
            maze[x][y] = "P"

    # ✅ แสดงแผนที่ใหม่
    print("\nเส้นทางที่เดิน:")
    for row in maze:
        print("".join(row))