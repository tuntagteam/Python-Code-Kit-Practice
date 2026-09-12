n = int(input("Enter your number :"))
sum = 0 #เก็บผลรวมของ 1 -> n
for i in range(1,n+1):
    print("ค่าของ i =",i)
    sum += i
    print("ค่าของ Sum =",sum)
print("ผลลัพธ์",sum)

for j in range(1,n+1):
    if j % 2 == 0:
        print(j)

