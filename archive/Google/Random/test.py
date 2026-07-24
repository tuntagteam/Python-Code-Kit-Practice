import random
number = random.randint(0,100)
gn = int(input("guess number"))
tries = 0
while gn != number:
    print("NOOOOOO lavaca policta wrong")
    if gn > number:
        print("NO LOWER LOVAC POLICITA")
    elif gn < number:
        print("NOOOOOOO mre more")
    gn = int(input("guess number again"))
    tries = tries+1
print("ok eat apple",tries)