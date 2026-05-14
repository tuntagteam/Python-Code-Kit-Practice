# # 7. ระบบตรวจจับเสียงสะท้อน

# นักวิทยาศาสตร์บันทึกคลื่นเสียงออกมาเป็นข้อความ

# หากข้อความมีตัวอักษรซ้ำติดกัน  
# แสดงว่าเกิด “เสียงสะท้อน”

# จงตรวจสอบว่ามีหรือไม่

# ## Input
# ข้อความ 1 บรรทัด

# ## Output
# YES หรือ NO

# ## Example

# ### Input
# helloo

# ### Output
# YES

# ### Input
# long

# ### Output
# NO
# ---

x=input()
a=0
for i in range(len(x) - 1):
    if x[i] == x[i+1]:
        a = 1
if a == 0:
    print("no")
elif a == 1:
    print("Yes")

# PS C:\Users\TagTrueCodingJr\Documents\GitHub\Python-Code-Kit-Practice> & C:/Python313/python.exe c:/Users/TagTrueCodingJr/Documents/GitHub/Python-Code-Kit-Practice/CodeKit2026/pace/test/7.py
# hello
# Traceback (most recent call last):
#   File "c:\Users\TagTrueCodingJr\Documents\GitHub\Python-Code-Kit-Practice\CodeKit2026\pace\test\7.py", line 35, in <module>
#     if y[i] == y[i+1]:
#        ~^^^
# TypeError: 'int' object is not subscriptable