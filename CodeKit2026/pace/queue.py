# JOIN x = ต่อคิว
# SERVE = คนด้านหน้าออกจากแถว

#เข้ามาจากด้านหลัง จะออกไปทางด้านหน้า


# JOIN 10 == [10]
# JOIN 20 == [10,20]
# SERVE == [20]
# JOIN 30 == [20,30]
# SERVE == [30]
# SERVE == []
# JOIN 40 == [40]
# [40]
# Output 10 20 30

# 3.โรงอาหารอัจฉริยะ 
# โรงอาหารแห่งหนึ่งมีระบบต่อคิวอาหาร 
# จะมีเหตุการณ์ 2 แบบ 
# JOIN x 
# หมายถึง นักเรียนหมายเลข x มาต่อคิว 
# SERVE 
# หมายถึง เรียกคนหน้าแถวออกไปรับอาหาร 
# ถ้ามี SERVE ตอนคิวว่าง ให้ข้ามไป 
# จงแสดงลําดับนักเรียนที่ได้รับอาหารจริง 
# Input 
# บรรทัดแรก จํานวนเหตุการณ์ n 
# จากนั ้นอีก n บรรทัดเป็นคําสั่ง 
# Output 
# แสดงหมายเลขนักเรียนที่ได้รับอาหาร 
# Example 
# Input 
# 6 
# JOIN 10 
# JOIN 20 
# SERVE 
# JOIN 30 
# SERVE 
# SERVE 
# Output 
# 10 20 30

x = int(input())
queue = []
served = []
for i in range(x):
    z = input().split() # JOIN 10 = [JOIN , 10] == [10]
    if z[0] == "JOIN":
        queue.append(z[1])

    elif z[0] == "SERVE":
        if queue:
            served.append(queue.pop(0))

print(*served)