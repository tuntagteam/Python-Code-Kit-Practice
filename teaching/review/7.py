num = int(input("input: "))
is_prime = True

if num < 2:
    is_prime = False
else:
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            is_prime = False
            break

if is_prime:
    print("เป็นจำนวนเฉพาะ")
else:
    print("ไม่เป็นจำนวนเฉพาะ")