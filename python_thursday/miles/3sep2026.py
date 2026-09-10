name = input("Enter your name : ")
age = int(input("Enter your age : "))
print("Hello,",name)
print("Next year you will be",age+1,"years old")

length = int(input("Enter length : "))
width = int(input("Enter width : "))
print(f"Area is {length*width}")

number = int(input("Enter your desired number : "))
if number % 2 == 0:
    print("Even")
else:
    print("Odd")

number2 = int(input("Enter your desired number 2 : "))
if number2 > 0:
    print("Positive")
elif number2 < 0:
    print("Negative")
else:
    print("Zero")