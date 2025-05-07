n = 4
if n <= 1:
    print("Not a prime")
else:
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            print("Not a prime")
            break
    else:
        print("Prime number")