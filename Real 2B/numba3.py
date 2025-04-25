n = int(input())  # จำนวนกล่อง

packages = []
# อ่านข้อมูลแต่ละกล่อง
for _ in range(n):
    name, urgency, area = input().split()
    urgency = int(urgency)
    area = int(area)
    packages.append((name, urgency, area))

# เรียงข้อมูลด้วย sorted โดยใช้ key ตามลำดับเงื่อนไข
sorted_packages = sorted(packages, key=lambda x: (x[1], x[2], x[0]))

# แสดงชื่อเรียงตามลำดับ
for package in sorted_packages:
    print(package[0])