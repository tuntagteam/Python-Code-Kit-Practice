import pandas as pd

# 1. รับค่า n จากผู้ใช้
n = int(input("Enter n: ").strip())

# 2. สร้าง DataFrame สำหรับสูตรคูณ
df = pd.DataFrame({
    'Multiplier': range(1, 26),
})
df['Result'] = df['Multiplier'] * n

# 3. แสดงตารางสูตรคูณโดยไม่แสดงดัชนี
print(df.to_string(index=False))

# 4. คำนวณผลรวมของคอลัมน์ Result แล้วแสดง
total = df['Result'].sum()
print(f"\nTotal = {total}")