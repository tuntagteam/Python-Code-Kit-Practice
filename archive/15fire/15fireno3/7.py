k = int(input().strip())
s = input().rstrip('\n')

result = []
for ch in s:
    # พิมพ์ใหญ่
    if 'A' <= ch <= 'Z':
        new_ord = (ord(ch) - ord('A') - k) % 26 + ord('A')
        result.append(chr(new_ord))
    # พิมพ์เล็ก
    elif 'a' <= ch <= 'z':
        new_ord = (ord(ch) - ord('a') - k) % 26 + ord('a')
        result.append(chr(new_ord))
    else:
        # ตัวอื่นคงเดิม
        result.append(ch)

print(''.join(result))