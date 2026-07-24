n = int(input("Enter a number (0-9): "))
words = ['ศูนย์', 'หนึ่ง', 'สอง', 'สาม', 'สี่', 'ห้า', 'หก', 'เจ็ด', 'แปด', 'เก้า']
if 0 <= n <= 9:
    print("Thai word:", words[n])
else:
    print("Invalid input.")