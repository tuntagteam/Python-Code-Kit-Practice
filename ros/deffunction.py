# Parameter = สิ่งที่ฟังก์ชันต้องการ
# Argument = สิ่งที่ส่งให้ฟังก์ชัน


# 1 ตัวเลขที่ 1
# 2 ตัวเลขที่ 2
# - + * / เครื่องหมาย
# 3

def add(x,y):
    return x+y

def minus(x,y):
    return x-y

def multiply(x,y):
    return x*y

def divided(x,y):
    return x/y

argument1 = int(input("Enter first number :"))
argument2 = int(input("Enter second number :"))
z = input("Enter operand (+,-,*,/):")

if z == "+":
    print(add(argument1,argument2))
elif z == "-":
    print(minus(argument1,argument2))
elif z == "*":
    print(multiply(argument1,argument2))
elif z == "/":
    print(divided(argument1,argument2))