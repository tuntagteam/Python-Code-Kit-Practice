# ฟังก์ชันแปลงตัวเลขเป็นเลขโรมัน
def int_to_roman(num):
    # จัดลำดับคู่ค่าเลขโรมันและค่าจำนวนเต็ม (หลัก Subtractive Notation)
    val_map = [
        (1000, 'M'),
        (900,  'CM'),
        (500,  'D'),
        (400,  'CD'),
        (100,  'C'),
        (90,   'XC'),
        (50,   'L'),
        (40,   'XL'),
        (10,   'X'),
        (9,    'IX'),
        (5,    'V'),
        (4,    'IV'),
        (1,    'I'),
    ]
    roman = []
    for val, sym in val_map:
        # นับว่ามีกี่ครั้งที่จะใช้สัญลักษณ์นี้
        count = num // val
        roman.append(sym * count)
        num %= val
        if num == 0:
            break
    return ''.join(roman)

# อ่านค่าและแปลง
n = int(input().strip())
print(int_to_roman(n))