import numpy as np

# กำหนดข้อมูล
44

# 1. ค่าเฉลี่ยอุณหภูมิ
mean_temp = temps.mean()

# 2. หาวันและค่าอุณหภูมิสูงสุด
idx_max = temps.argmax()
max_date = dates[idx_max]
max_temp = temps[idx_max]

# 3. สร้างอาร์เรย์ Above_Average
above_average = temps > mean_temp

# 4. แสดงตารางผลลัพธ์
print(f"{'Date':<12}{'Temp':<6}{'Above_Avg'}")
for d, t, a in zip(dates, temps, above_average):
    flag = 'Yes' if a else 'No'
    print(f"{str(d):<12}{t:<6}{flag}")

# 5. สรุปผล
print(f"\nMean temperature: {mean_temp:.2f}")
print(f"Highest on: {max_date} with {max_temp}")