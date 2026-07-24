x = int(input())

level = 1
while True:
    required = 10 ** level + level * 100
    if x < required:
        print(level - 1)  # เพราะ x ยังไม่ถึง required ของ level นี้ แปลว่าอยู่ level ก่อนหน้า
        print(required - x)  # จำนวนที่ต้องเติมเพื่อให้ไป level นี้
        break
    level += 1