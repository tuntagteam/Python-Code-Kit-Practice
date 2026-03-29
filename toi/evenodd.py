even = 0
odd = 0

def checkEvenOdd(num):
    global even , odd
    if num % 2 == 0:
        even += 1
    else:
        odd += 1

number = [] 

for j in range(3):
    a = int(input())
    number.append(a)

for i in number:
    checkEvenOdd(i)

print("even =",even)
print("odd",odd)