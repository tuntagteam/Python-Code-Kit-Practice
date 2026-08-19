sum = 0
for i in range(1,1000001):
    if i % 2 == 0:
        print(i,"Even")
        sum += i
    else:
        print(i,"Odd")
print("Total :",sum)