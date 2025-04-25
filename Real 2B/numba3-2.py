

# เรียงข้อมูลด้วย sorted โดยใช้ key ตามลำดับเงื่อนไข
sorted_packages = sorted(packages, key=lambda x: (x[1], x[2], x[0]))

[Nanon, 2, 5]
[Tawan, 1, 7]
[Boat, 2, 3]
[Taewon, 1, 7]


4
Nanon 2 5
Tawan 1 7
Boat 2 3
Taewon 1 7
