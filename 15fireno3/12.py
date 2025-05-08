n = int(input().strip())

# กรณีพิเศษเมื่อต้องการแปลง 0
if n == 0:
    print('0')
else:
    bits = []
    # แปลงโดยการหารเอาเศษ 2 ทีละขั้น
    while n > 0:
        bits.append(str(n % 2))
        n //= 2
    # เราเก็บบิตจากต่ำสุดไปหาสูงสุด จึงต้องกลับลำดับก่อนพิมพ์
    print(''.join(reversed(bits)))