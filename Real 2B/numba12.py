# ข้อมูลการยิง: 1 = ยิงโดน, 0 = ยิงพลาด
shots = [1, 1, 0, 0, 0, 0, 0, 0, 1, 0]

# ตัวแปรนับจำนวนที่ยิงโดน
hit_count = 0  # เริ่มจาก 0 ก่อน

# 🔁 วนลูปผ่านทุกการยิง
for shot in shots:
    if shot == 1:  # ถ้ายิงโดน
        hit_count += 1  # เพิ่มค่าตัวนับ

# หาจำนวนทั้งหมดของการยิง
total_shots = 0
for _ in shots:
    total_shots += 1  # นับจำนวนรอบใน list แบบไม่ใช้ len()

# คำนวณ Accuracy: จำนวนที่ยิงโดน / จำนวนทั้งหมด
accuracy = hit_count / total_shots  # ต้องเป็นทศนิยม ไม่ปัดเศษ

# แสดงผลลัพธ์ตามฟอร์แมต
print("ยิงโดนทั้งหมด:", hit_count, "นัด")
print("Accuracy:", accuracy)

# 🔍 ตรวจประเมินระดับความแม่น
if accuracy >= 0.7:
    print("ผลประเมิน: แม่นมาก!")
elif accuracy >= 0.4:
    print("ผลประเมิน: ก็โอเค")
else:
    print("ผลประเมิน: กระจอก")