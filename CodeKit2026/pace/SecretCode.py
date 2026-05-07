# 9. ระบบค้นหารหัสลับ 
# มีรหัสเรียงจากน้อยไปมากอยู่แล้ว 
# ให้ตรวจสอบว่ามีเลข x อยู่ในระบบหรือไม่ 
# ถ้ามีให้แสดงตําแหน่ง index 
# ถ้าไม่มีให้แสดง -1 
# เงื่อนไข 
# ต้องทําให้เร็วที่สุด 
# Example 
# Input 
# 6 
# 1 3 5 7 9 11 
# 7 
# Output 
# 3

x=int(input())
y=list(map(int, input().split()))
z=int(input())
index = -1
for i in range(x):
    if y[i] == z:
        index = i
        break

print(index)