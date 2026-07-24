m = int(input())

# หาความยาวของจำนวนหลัก
num_length = len(str(m))

# หาค่าขั้นต่ำของเลขที่มีหลักมากกว่าเดิม 1 หลัก
next_milestone = 10 ** num_length

# คำนวณจำนวนเงินที่ต้องเติมเพิ่ม
amount_to_add = next_milestone - m

print(amount_to_add)