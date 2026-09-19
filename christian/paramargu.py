def add(num1,num2):
    return num1 + num2

def minus(num1,num2):
    return num1 - num2

def multiply(num1,num2):
    return num1 * num2

def devided(num1,num2):
    return num1 / num2

def modulo(num1,num2):
    return num1 % num2

running = True

while running:
    print("==================")
    a = int(input("Enter the first number :"))
    b = int(input("Enter the second number :"))
    print("==================")
    print(f"What are you going to do with {a} and {b}")
    print("1. Plus")
    print("2. Minus")
    print("3. Multiply")
    print("4. Devided")
    print("5. Modulo")
    print("0. Exit the program")
    print("==================")
    z = int(input("Enter your choice :"))

    if z == 1:
        print(f"{a} + {b} = {add(a,b)}")
    elif z == 2:
        print(f"{a} - {b} = {minus(a,b)}")
    elif z == 3:
        print(f"{a} * {b} = {multiply(a,b)}")
    elif z == 4:
        print(f"{a} / {b} = {devided(a,b)}")
    elif z == 5:
        print(f"{a} % {b} = {modulo(a,b)}")
    elif z == 0:
        print("Good Bye!")
        running = False
    else:
        print("Please enter valid choices")
        print("==================")
        print(f"What are you going to do with {a} and {b}")
        print("1. Plus")
        print("2. Minus")
        print("3. Multiply")
        print("4. Devided")
        print("5. Modulo")
        print("0. Exit the program")
        print("==================")
        z = int(input("Enter your choice :"))