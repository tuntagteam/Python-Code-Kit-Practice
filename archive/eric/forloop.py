n = int(input("How many subject : "))
total = 0
passed = 0
failed = 0

for i in range(n):
    print("Enter your #",i+1,"score")
    score = int(input())
    if score >= 50:
        passed += 1
    else:
        failed += 1
    total += score

avg = total / n

print("==========")
print("Total : ", total)
print("Passed : ", passed)
print("Failed : ", failed)
print("Average : ", avg)
print("==========")