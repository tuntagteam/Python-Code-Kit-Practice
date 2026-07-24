numbor = 25
n = int(input("guess number: "))

while n != numbor:
    if n < numbor:
        print("too low, try a bigger number")
    elif n > numbor:
        print("too high, try a smaller number")
    n = int(input("guess number: "))

print("Correct! You guessed it.")