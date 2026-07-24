import numpy as np

# ข้อมูลเกรด
grades = np.array([60, 72, 85, 90, 68, 75, 88, 92, 55, 80])

# 1. ค่าเฉลี่ย
mean_value = grades.mean()

# 2. ค่ามัธยฐาน
median_value = np.median(grades)

# 3. ค่าเบี่ยงเบนมาตรฐาน
std_value = grades.std()  # ค่า ddof=0 (population)

# 4. ช่วง (range)
range_value = grades.max() - grades.min()

# แสดงผลลัพธ์
print(f"Mean: {mean_value:.2f}")
print(f"Median: {median_value:.2f}")
print(f"Std Dev: {std_value:.2f}")
print(f"Range: {range_value}")