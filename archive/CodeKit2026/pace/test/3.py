# # 3. ระบบปล่อยจรวดอัตโนมัติ

# ศูนย์อวกาศกำลังนับถอยหลังปล่อยจรวด

# หากตัวเลขในลิสต์ “ลดลง” จากค่าก่อนหน้า  
# แสดงว่าระบบผิดปกติทันที

# จงตรวจสอบว่าค่าทั้งหมดเรียงจากน้อยไปมากหรือไม่

# ## Input
# จำนวน n

# ตัวเลข n ตัว

# ## Output
# SORTED หรือ UNSORTED

# ## Example

# ### Input
# 5
# 1 2 2 5 9

# ### Output
# SORTED

# ---

x=int(input())
y=list(map(int, input().split()))
z=sorted(y)

if z == y:
    print("SORTED")
else:
    print("UNSORTED")