# UNDO = ยกเลิกอันล่าสุด
# DRAW = เพิ่มเข้าไปในลิสต์
# DRAW cat   -> [cat]
# DRAW dog   -> [cat, dog]
# UNDO       -> ลบ dog เหลือ [cat]
# DRAW fish  -> [cat, fish]
# DRAW bird  -> [cat, fish, bird]
# outout = cat fish bird

x = int(input())
y = []

for i in range(x):
    u = input().split()
    if u[0] == "DRAW":
        y.append(u[1])
    elif u[0]=="UNDO":
        y.pop()
    
print(*y)