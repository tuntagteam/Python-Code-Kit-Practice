import pandas as pd  # ใช้สำหรับจัดการข้อมูลแบบตาราง
from datetime import time  # ใช้สำหรับนิยามเวลาตัดสาย เช่น 10:30

# สร้างข้อมูลจำลองในรูปแบบ DataFrame
df = pd.DataFrame({
    'employee_id': ['E01', 'E01', 'E02', 'E02', 'E03', 'E03'],  # ID ของพนักงานแต่ละคน
    'date': ['2024-05-01', '2024-05-02'] * 3,  # วันที่ที่เข้างาน (วนลูป 2 วัน x 3 คน)
    'checkin_time': ['10:55', '10:35', '10:39', '10:40', '11:00', '10:49']  # เวลาที่เช็กอิน (เป็น string)
})

# แปลง checkin_time จาก string เป็นชนิดเวลา (datetime.time) เพื่อให้เปรียบเทียบเวลาได้
df['checkin_time'] = pd.to_datetime(df['checkin_time'], format='%H:%M').dt.time

# นิยามเวลาตัดสาย = 10:30 AM (หลังจากนี้ถือว่าสาย)
cutoff_time = time(10, 30)

# เพิ่มคอลัมน์ใหม่ชื่อ 'late' ซึ่งมีค่าเป็น True/False ว่ามาสายหรือไม่
df['late'] = df['checkin_time'] > cutoff_time
# ถ้าเวลาเช็กอิน > 10:30 จะได้ค่า True → สาย
# ถ้า <= 10:30 จะได้ค่า False → ไม่สาย

# 🔹 ส่วนที่ 1: หาพนักงานที่มาสายบ่อยที่สุด
# กรองเฉพาะแถวที่มาสาย (late == True)
late_df = df[df['late']]

# groupby ตาม employee แล้วนับจำนวนแถว (size) → คือจำนวนครั้งที่มาสาย
late_counts = late_df.groupby('employee_id').size()

# ตรวจว่ามีใครมาสายบ้างหรือไม่
if not late_counts.empty:
    most_late_emp = late_counts.idxmax()  # หา employee_id ที่มาสายบ่อยที่สุด
    most_late_times = late_counts.max()   # จำนวนครั้งที่มาสายมากที่สุด
    print(f"พนักงานที่มาสายบ่อยที่สุด: {most_late_emp} ({most_late_times} ครั้ง)")
else:
    print("ไม่มีใครมาสายเลย!")

# 🔹 ส่วนที่ 2: หาพนักงานที่ไม่เคยมาสายเลย
# รายชื่อพนักงานทั้งหมดใน DataFrame
all_employees = df['employee_id'].unique()

# คัดเฉพาะคนที่ไม่มีอยู่ใน late_counts → คือไม่เคยมาสาย
on_time_employees = [emp for emp in all_employees if emp not in late_counts.index]

# แสดงผลผู้ที่ไม่เคยมาสาย
if on_time_employees:
    print("พนักงานที่ไม่เคยมาสาย:", ", ".join(on_time_employees))
else:
    print("ทุกคนเคยมาสายหมด")

# 🔹 ส่วนที่ 3: สร้าง Pivot Table แสดงสถานะการมาสายรายวัน
# - index = employee_id → แถวคือพนักงาน
# - columns = date → คอลัมน์คือวันที่
# - values = late → ค่าในตารางคือ True/False ว่ามาสายหรือไม่
pivot = df.pivot_table(index='employee_id', columns='date', values='late', aggfunc='first')

# แสดงผล Pivot Table พร้อมเติม '-' แทน NaN (ถ้าไม่ได้เข้างานวันนั้น)
print("\nPivot Table:")
print(pivot.fillna('-'))