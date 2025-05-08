def is_perfect(n):
    # ถ้า n = 1 → ไม่ถือเป็น Perfect Number (ผลรวมตัวประกอบ = 0)
    if n <= 1:
        return False
    total = 1  # เริ่มจาก 1 เพราะ 1 เป็นตัวประกอบเสมอ (ไม่นับตัวมันเอง)
    # ตรวจตัวประกอบจาก 2 จนถึง sqrt(n)
    i = 2
    while i * i <= n:
        if n % i == 0:
            total += i
            # ถ้า i ไม่เท่ากับ n//i ก็ให้บวกตัวประกอบอีกตัว
            if i != n // i:
                total += n // i
        i += 1
    return total == n

if __name__ == "__main__":
    n = int(input().strip())
    if is_perfect(n):
        print("เป็น Perfect Number")
    else:
        print("ไม่เป็น Perfect Number")