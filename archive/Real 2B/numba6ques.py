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

# TODO 1: เขียนฟังก์ชัน bfs(start, end) เพื่อหาทางไปหาลูกค้า
# - ใช้ BFS เดินได้แค่ ".", "C"
# - ห้ามเดินทับ "#" หรือ "*"
# - ต้อง return จำนวนก้าวที่สั้นที่สุด หากเดินได้

# TODO 2: หลังจากเดินได้แล้ว ย้อนทางกลับจาก C -> S แล้ว mark จุดเดินด้วย 'P'
# - อย่า mark จุด S หรือ C

# TODO 3: แสดงผลลัพธ์ เช่น:
# - "สามารถส่งอาหารได้ใน X ก้าว"
# - หรือ "ส่งอาหารไม่สำเร็จ"
# - และพิมพ์แผนที่ออกมา

# ตัวอย่างการแสดงแผนที่ (แค่ไกด์):
# S.P.......
# .P........
# .P*.#.....
# ###P......
# ...#PC....