user_input = input("Enter a value: ")
x = int(user_input)

level = 0
while True:
    xp = 10 ** level + level * 100
    if x < xp:
        print(level - 1)  # เพราะ x ยังไม่ถึง required ของ level นี้ แปลว่าอยู่ level ก่อนหน้า
        print(xp - x)  # จำนวนที่ต้องเติมเพื่อให้ไป level นี้
        break
    level += 1