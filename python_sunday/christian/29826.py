import random

x = random.randint(1,100)
y = int(input("Guess the number : "))
attempt = 0
while x != y:
    print("Incorrect! Try again.")
    if y > x:
        print("Too high!")
    else:
        print("Too low!")
    y = int(input("Guess the number : "))
print("Correct! You're good!")