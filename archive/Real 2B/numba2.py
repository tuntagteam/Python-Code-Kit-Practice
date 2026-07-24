x = int(input())  # รับจำนวนเหรียญเริ่มต้น

total_special = 0  # จำนวนเหรียญพิเศษทั้งหมดที่สะสมได้
current_coins = x  # เหรียญที่มีในแต่ละรอบ (รวมปกติ + พิเศษ)

while current_coins >= 9:
    new_special = current_coins // 9             # แลกได้กี่เหรียญพิเศษในรอบนี้
    total_special += new_special                 # เพิ่มเข้าไปในยอดรวม
    current_coins = new_special + (current_coins % 9)  # เหรียญที่เหลือในรอบถัดไป

print(total_special)

