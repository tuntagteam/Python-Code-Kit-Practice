user = input("Enter your name : ")
print("Your name is " + user)


score = int(input("Enter your score : "))
if score >= 80:
    print("Grade A")
elif score >= 70:
    print("Grade B")
elif score >= 60:
    print("Grade C")
elif score >= 50:
    print("Grade D")
else:
    print("Grade F")

n = int(input("Enter N :"))
count = 0
sum = 0
for i in range(n):
    if i % 2 == 0:
        sum += i
        count += 1
        print(i)
    

print("Count : " , count)
print("Sum : " ,sum)

g = int(input("Enter G: "))
i = 1

while i <= 12:
    print(f"{g} x {i} = {g * i}")
    i += 1