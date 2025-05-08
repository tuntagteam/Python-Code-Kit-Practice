def is_armstrong(n):
    # แปลง n เป็น list ของหลักแต่ละหลัก
    digits = [int(d) for d in str(n)]
    power = len(digits)  # จำนวนหลัก
    # คำนวณผลรวมของแต่ละหลักยกกำลังด้วยจำนวนหลัก
    total = sum(d**power for d in digits)
    return total == n

n = int(input().strip())
if is_armstrong(n):
    print("เป็น Armstrong Number")
else:
    print("ไม่เป็น Armstrong Number")