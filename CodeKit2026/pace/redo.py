# 4.ระบบย้อนคําสั ่งล่าสุด 
# โปรแกรมวาดรูปของเด็ก ๆ มีระบบเก็บคําสั่ง 
# จะมีคําสั่ง 2 แบบ 
# DRAW x 
# วาดรูปชื่อ x 
# UNDO 
# ยกเลิกรูปล่าสุดที่วาด 
# หากยังไม่มีรูปใดเลย แล้วเจอ UNDO ให้ข้ามไป 
# หลังจบทุกคําสั่ง ให้แสดงรูปที่ยังเหลืออยู่ตามลําดับ 
# Example 
# Input 
# 5 
# DRAW cat 
# DRAW dog 
# UNDO 
# DRAW fish 
# DRAW bird 
# Output 
# cat fish bird

x = int(input())
z=[]
u=[]
for i in range(x):
    y = input().split()
    if y[0] == "DRAW":
        z.append(y[1])
    elif y[0] == "UNDO":
        z.pop()
print(*z)


